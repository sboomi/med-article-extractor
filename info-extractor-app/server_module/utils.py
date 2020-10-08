import re
from tika import parser
from pymed.pymed import PubMed, retrieve_informations
from collections import defaultdict
from bs4 import BeautifulSoup
from server_module import db
from server_module.models import Article


def get_pdf_content(pdf_file):
    raw = parser.from_file(pdf_file, xmlContent=True)
    return BeautifulSoup(raw['content'], 'lxml'), raw['metadata']


def extract_pdf_information(soup, metadata):
    regex_journal = r"( *[A-Z][a-z]+ *)(of|and|[:&])*"

    subject = find_subject_content(metadata)

    if subject and len(subject) <= 20:
        matches = re.finditer(regex_journal, subject)
        for i, match in enumerate(matches):
            if i == 0:
                start_str = match.start()
            end_str = match.end()
        journal = subject[start_str:end_str]
    else:
        journal = ""

    data = {
        "title": metadata['title'] if 'title' in metadata else "",
        "publication_date": metadata['Creation-Date'] if 'Creation-Date' in metadata else "",
        "keywords": metadata['Keywords'] if 'Keywords' in metadata else "",
        "abstract": subject if len(subject) > 200 else "",
        "journal": journal,
        "doi": find_doi(metadata),
        "authors": metadata["Author"] if 'Author' in metadata else "",
        "wordcount": get_word_count(soup.text),
        "aav_terms": get_aav_count(soup.text),
        "ref_publications": get_ref_count(soup)
    }
    return data


def get_pubmed_info(title):
    pm = PubMed()
    url_id = pm.fetch(title, retrieve_mode='xml')
    obj_results = retrieve_informations(url_id, format="xml")
    data_dict = pm.return_information(obj_results)
    return data_dict


def find_subject_content(metadata):
    subject = ""
    if 'cp:subject' in metadata:
        subject = metadata['cp:subject']
    else:
        for k in metadata.keys():
            if "subject" in k.lower():
                subject = metadata[k]

    return subject


def find_doi(metadata):
    doi = ""
    if 'doi' in metadata:
        doi = metadata['doi']
    else:
        for v in metadata.values():
            if "doi:" in v:
                doi = re.search(r"doi:\S+", v)
                doi = doi.replace("doi:", "")
    return doi


def get_aav_count(text):
    regex_aav = r"AAV(\d*\/|\d*-)*\w*(\([\w, -]*\))*(-\w+)*"
    d = defaultdict(int)
    for match in re.finditer(regex_aav, text, re.M):
        d[match.group(0)] += 1
    return {k:v for k,v in d.items()}


def get_ref_count(soup):
    ref_reg = r"^\d+( *\**\.)* ([A-Z]\S* ([A-Z]\S* )*[A-Z]\w*(, )*)+"
    regex_aav = r"AAV(\d*\/|\d*-)*\w*(\([\w, -]*\))*(-\w+)*"
    rel_publ = []
    for el in soup.find_all('p'):
        if re.search(ref_reg, el.text, re.M) and re.search(regex_aav, el.text, re.M | re.I):
            rel_publ.append(el.text)
    return rel_publ


def get_word_count(text):
    list_words = [word for word in re.split(r"\s", text) if word]
    return len(list_words)


def return_information_as_batch(id_list, source_db, batch_size=20, db_output="sql"):
    count = 0

    if type(batch_size) is float and 0 < batch_size < 1:
        batch_size = len(id_list) * batch_size
    batch_ids = [",".join(id_list[portion:portion + batch_size]) for portion in range(0, len(id_list), batch_size)]

    for batch in batch_ids:
        url = source_db.fetch(batch)
        if len(url) > 2000:
            raise Exception("Error: URL too long. Please select a lower batch size.")
        soup = retrieve_informations(url, format='xml')
        data = source_db.return_information(soup, as_dataframe=False)
        if db_output == "sql":
            for i in range(len(data['pubmed_id'])):
                if not Article.query.filter_by(pubmed_id=data['pubmed_id'][i]).first():
                    article = Article(pubmed_id=int(data['pubmed_id'][i]),
                                      abstract=data['abstract'][i],
                                      title=data['title'][i],
                                      publication_date=data['publication_date'][i],
                                      keywords=data['keywords'][i],
                                      doi=data['doi'][i],
                                      authors=data['authors'][i])
                    db.session.add(article)
                    db.session.commit()
                    count += 1
    return f"{count} out of {len(id_list)} uploaded!"
