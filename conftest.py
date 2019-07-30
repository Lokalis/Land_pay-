from Application.SynergyApp import App
import pytest
import allure
from urllib.parse import urlparse
import requests
from Tests.test_land import *


CLI_LAND_URL = '--land-url'


@pytest.fixture()
def synergypay():
    """TODO: Add fixture teardown, which delete order in 1001 ticket with api.
    (Go to Postman)"""
    app=App()
    yield
    # if len(order_number)!=0:
    #     app.open_page("https://yandex.ru")
    app.destroy()


def pytest_addoption(parser):
    parser.addoption(CLI_LAND_URL, help='URL to Synergy land for test', required=True)

@pytest.fixture(scope='session')
def land_url(request):
    ''' get url of land under test '''
    url = request.config.getoption(CLI_LAND_URL)
    if not urlparse(url).scheme:
        url = 'https://' + url
    assert requests.get(url).status_code==200,f'Status code page {url} - {requests.get(url).status_code}'
    return url