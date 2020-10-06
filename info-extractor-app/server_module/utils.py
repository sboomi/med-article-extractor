import os
import re
import datetime
from tika import parser
from pymed.pymed import PubMed, retrieve_informations
from collections import defaultdict
import json
from bs4 import BeautifulSoup


def get_pdf_content(pdf_file):
    raw = parser.from_file(pdf_file, xmlContent=True)
    return BeautifulSoup(raw, 'lxml')


def evaluate_pdf(soup):
    pass
