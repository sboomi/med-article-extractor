import os
import re
from tika import parser
from pymed.pymed import PubMed, retrieve_informations
from collections import defaultdict
import json

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
df = pm.return_information(obj_results)

#PDF extraction
wordcount = []
aav_terms = {}

regex_aav = r"AAV(\d*/|\d*-)*\w*(\([\w, -]*\))*(-\w+)*"

for id, pdf in zip(df["pubmed_id"].values, list_pdf):
    filename = os.path.join(pdf_path,pdf)
    d = defaultdict(int)
    raw = parser.from_file(filename)
    s = raw['content']
    wordcount.append(len(s))

    for match in re.finditer(regex_aav, s, re.M):
        d[match.group(0)] += 1
    aav_terms[str(id)] = {str(k): v for k,v in d.items()}

df["wordcount"] = wordcount
df.to_excel("sample/publication_info.xlsx", index=None)

with open("sample/aav_info.json", "w", encoding="utf-8") as file:
    json.dump(aav_terms, file, ensure_ascii=False, indent=4)