import pytest
import os

from src.class_company import Company
from src.class_vacancy import Vacancy
from env import DB_HOST, DB_NAME, USER, PASSWORD, DB_PORT


@pytest.fixture()
def dict_company():
    return {'test_1': {'name': 'test_1',
                       'alternate_url': 'url_1',
                       'accredited_it_employer': True},
            'test_2': {'name': 'test_2',
                       'alternate_url': 'url_2',
                       'accredited_it_employer': True}}


@pytest.fixture()
def dict_vacancy():
    return {'test_1': [{'id': 1,
                        'name': 'vac_1',
                        'alternate_url': 'vac_url_1',
                        'salary': {'from': None, 'to': 100},
                        'city': 'Mos1',
                        'published_date': '2024-01-01',
                        'experience': '1',
                        'requirement': 'va1'}],
            'test_2': [{'id': 2,
                        'name': 'vac_2',
                        'alternate_url': 'vac_url_2',
                        'salary': {'from': 200, 'to': None},
                        'city': 'Mos2',
                        'published_date': '2024-02-02',
                        'experience': '2',
                        'requirement': 'va2'}]}


@pytest.fixture()
def data_company():
    return {'test_1': Company('com_1', 'http_url_1', True),
            'test_2': Company('com_2', 'http_url_2', True)}


@pytest.fixture()
def data_vacancy():
    return {'test_1': [Vacancy(1, 'vac_1', 'http_url_1', {'from': None, 'to': 100}, 'Mos1', '2024-01-01', '1', 'va1')],
            'test_2': [Vacancy(2, 'vac_2', 'http_url_2', {'from': None, 'to': 200}, 'Mos2', '2024-02-02', '2', 'va2')]}


@pytest.fixture()
def get_database_name():
    return DB_NAME


@pytest.fixture()
def get_params():
    return {'host': DB_HOST,
            'user': USER,
            'password': PASSWORD,
            'port': DB_PORT}
