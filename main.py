import pandas as pd
import string
import requests as requests
from bs4 import BeautifulSoup
import numpy as np


def get_and_clean_data():
    data = pd.read_csv('software_developer_united_states_1971_20191023_1.csv')
    description = data['job_description']
    cleaned_description = description.apply(lambda s: s.translate(str.maketrans('', '', string.punctuation + u'\xa0')))
    cleaned_description = cleaned_description.apply(lambda s: s.lower())
    cleaned_description = cleaned_description.apply(lambda s: s.translate(str.maketrans(string.whitespace, ' '*len(string.whitespace), '')))
    cleaned_description = cleaned_description.drop_duplicates()
    return cleaned_description

def simple_tokenize(data) :
    cleaned_description = data.apply(lambda s: [x.strip() for x in s.split()])
    return cleaned_description

def parse_job_description():
    cleaned_description = get_and_clean_data()
    cleaned_description = simple_tokenize(cleaned_description)
    return cleaned_description

def count_python_mysql():
    parsed_description = parse_job_description()
    count_python = parsed_description.apply(lambda s: 'python' in s).sum()
    count_mysql = parsed_description.apply(lambda s: 'mysql' in s).sum()
    print('python: ' + str(count_python) + ' of ' + str(parsed_description.shape[0]))
    print('mysql: ' + str(count_mysql) + ' of ' + str(parsed_description.shape[0]))

def parse_db():
    html_doc = requests.get("https://www.improgrammer.net/top-10-databases-should-learn-2015/").content
    soup = BeautifulSoup(html_doc, 'html.parser')
    all_db = [s.get_text() for s in soup.findAll('dt')]
    db_list = [s.lower() for s in all_db]
    db_list = [[x.strip() for x in s.split()] for s in db_list]
    return db_list

def after_python_lesson() :
    parsed_db = parse_db()
    parsed_description = parse_job_description()
    with_python = [None] * len(parsed_db)
    for i,db in enumerate(parse_db()) :
        with_python[i] = parsed_description.apply(lambda s: np.all([x in s for x in db]) and 'python' in s).sum()
        print(' '.join(db) + ' + python: ' + str(with_python[i]) + ' of ' + str(parsed_description.shape[0]))
