import os
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import re

class GoogleScholar:
    def __init__(self):
        self.url = "https://scholar.google.fr/"
        self.browser = webdriver.Firefox()

    def generate_dataframe(self):
        data = {"title": [],
        "summary": [],
        "complementary_info": [],
        "pdf_link": []
        }
        return data

    def get_query(self,keywords,locale='fr',n_page=1):
        if not keywords:
            print("Error: no keywords inserted")
            return None
        query = "+".join(keywords)
        return f"{self.url}scholar?start={(n_page-1)*10}&hl={locale}&as_sdt=0%2C5&q={query}&btnG="

    def download_pdf(self, link, filename, chunk_size=2000):
        if os.path.exists(f"pdf-samples/{filename}.pdf"):
            return f"{filename}.pdf already exists!"
        try:
            r = requests.get(link, stream=True)
        except requests.exceptions.ConnectionError:
            return "Something went wrong with the connection. Aborting..."
        else:
            with open(f"pdf-samples/{filename}.pdf", "wb") as file:
                for chunk in r.iter_content(chunk_size):
                    file.write(chunk)
            return f"{filename}.pdf downloaded!"

    def navigate_and_get_pdfs(self, keywords, n_pages=1):
        for i in range(1,n_pages+1):
            url_req = self.get_query(keywords, n_page=i)
            self.browser.get(url_req)

            entries = self.browser.find_elements_by_css_selector("div.gs_r.gs_or.gs_scl")
            for entry in entries:
                main_content = entry.find_element_by_css_selector("div.gs_ri")
                title = main_content.find_element_by_tag_name("h3").text
                try:
                    pdf_section=entry.find_element_by_css_selector('div.gs_or_ggsm')
                except NoSuchElementException:
                    print("No PDF available")
                else:
                    if "[PDF]" in pdf_section.text:
                        link = pdf_section.find_element_by_tag_name('a').get_attribute('href')
                        filename="".join([word.capitalize() for word in re.split(r'\W',title) if word])
                        print(self.download_pdf(filename,link))
                    else:
                        print("Link is avaiable but it's not PDF")

            
        self.browser.quit()
        return "Done!"

    def reload_browser(self):
        self.browser = webdriver.Firefox()
