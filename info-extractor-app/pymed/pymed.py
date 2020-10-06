import requests
import json
import lxml
from bs4 import BeautifulSoup
from bs4 import FeatureNotFound
import re
import pandas as pd
from datetime import datetime

class PubMed:
    def __init__(self):
        self.url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.db = "pubmed"

    def search(self, terms, max_req=20, sort_type="relevance", retrieve_mode="json"):
        search_url = f"esearch.fcgi?db={self.db}"
        term_plus = ["+".join(term.split()) for term in terms]
        term_url = "&term=" + "+AND+".join(term_plus)
        sort_url = f"&sort={sort_type}"
        max_url = f"&retmax={max_req}"
        ret_url = f"&retmode={retrieve_mode}"
        return self.url + search_url + term_url + max_url + sort_url + ret_url

    def fetch(self, id_list, retrieve_mode="json"):
        fetch_url = f"efetch.fcgi?db={self.db}"
        id_url = f"&id={','.join(id_list)}"
        ret_url = f"&rettype={retrieve_mode}"
        return self.url + fetch_url + id_url + ret_url

    def retrieve_id_by_title(self, title):
        search_url = f"esearch.fcgi?db={self.db}"
        retmode_url = "&retmode=json"
        field_url = "&field=title"
        term_url = f"&term={title}"
        full_url = self.url + search_url + retmode_url + term_url + field_url
        r = requests.get(full_url).content
        content = json.loads(r)
        return content['esearchresult']['idlist'] if content['esearchresult']['idlist'] else None

    def return_information(self, soup, as_dataframe=False):
        data_info = {
            'title' : [],
            'abstract' : [],
            'pubmed_id' : [],
            'publication_date' : [],
            'keywords' : [],
            'journal' : [],
            'doi' : [],
            'authors' : []
        }


        for article in soup.find_all('pubmedarticle'):
            data_info['title'].append(article.articletitle.text)
            data_info['abstract'].append(article.abstract.text)
            data_info['pubmed_id'].append(int(article.pmid.text))
            data_info['publication_date'].append( datetime.strptime("/".join(article.find('pubmedpubdate', {"pubstatus" : "pubmed"}).text.split()), '%Y/%m/%d/%H/%M') )
            try:
                data_info['keywords'].append(", ".join(article.keywordlist.text.split()))
            except:
                print("No keywords available for this article")
                data_info['keywords'].append("")

            try:    
                data_info['journal'].append(article.journal.title.text.strip() + ', ' + article.journal.isoabbreviation.text.strip())
            except:
                print("Journal not found. Trying Medline instead.")
                try:
                    data_info['journal'].append(article.medlinejournalinfo.medlineta.text)
                except:
                    print("No journal found")
                    data_info['journal'].append("")
            
            try:
                data_info['doi'].append(article.find('elocationid', {'eidtype': 'doi'}).text)
            except:
                print("Error : couldn't find the DOI")
                data_info['doi'].append("")

            data_info['authors'].append(", ".join([author.initials.text + ". " + author.lastname.text for author in article.find_all('author') if author.lastname]))

        if as_dataframe:
            df = pd.DataFrame(data_info)
            return df
        else:
            return data_info


class PMC(PubMed):
    def __init__(self):
        self.url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.db = "pmc"



def retrieve_informations(link, format="json"):
    r = requests.get(link).content
    if format=="json":
        return json.loads(r)
    if format=="xml":
        try:
            return BeautifulSoup(r, 'lxml')
        except FeatureNotFound:
            print("""Parser not found. Please install parser using 

pip install lxml

And relaunch the script
            """)
