import os
import re
import datetime
from tika import parser
from pymed.pymed import PubMed, retrieve_informations
from collections import defaultdict
import json
from bs4 import BeautifulSoup

pdf_path = "sample/pdfs"
list_pdf = os.listdir(pdf_path)
title_regex = r"^\d{4}_(.+)\.pdf"

list_titles = [re.search(title_regex, pdf).group(1) for pdf in list_pdf]

pm = PubMed()
list_ids = []

for title in list_titles:
    id_article = pm.retrieve_id_by_title(title)
    if id_article:
        list_ids.append(id_article[0])
    else:
        print("Information not found. Article isn't available on PubMed")


url_ids = pm.fetch(list_ids, retrieve_mode='xml')
obj_results = retrieve_informations(url_ids, format="xml")
data_dict = pm.return_information(obj_results)


#PDF extraction
wordcount = []
aav_terms = []
ref_publications = []

regex_aav = r"AAV(\d*\/|\d*-)*\w*(\([\w, -]*\))*(-\w+)*"
ref_reg = r"^\d+( *\**\.)* ([A-Z]\S* ([A-Z]\S* )*[A-Z]\w*(, )*)+"

for pdf in list_pdf:
    filename = os.path.join(pdf_path,pdf)
    d = defaultdict(int)
    rel_publ = []

    raw = parser.from_file(filename, xmlContent=True)
    soup = BeautifulSoup(raw['content'], 'lxml')
    wordcount.append(len(soup.text))

    for match in re.finditer(regex_aav, soup.text, re.M):
        d[match.group(0)] += 1
    aav_terms.append({k: v for k,v in d.items()})

    for el in soup.find_all('p'):
        if re.search(ref_reg,el.text,re.M) and re.search(regex_aav,el.text,re.M | re.I):
            rel_publ.append(el.text)
    ref_publications.append(rel_publ)

data_dict["wordcount"] = wordcount
data_dict["aav_terms"] = aav_terms
data_dict["ref_publications"] = ref_publications  


with open("sample/pdf_data.json", "w", encoding="utf-8") as file:
    for i in range(len(data_dict["pubmed_id"])):
        json_data = {str(k):(str(v[i]) if isinstance(v[i], datetime.datetime) else v[i]  ) for k,v in data_dict.items()}
        try:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        except TypeError:
            print("""Error, types authorized by JSON are 
int, float, bool, str, dict, list, None

Please run type(obj) to check if the types are fitting
            """)