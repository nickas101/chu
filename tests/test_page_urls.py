import pytest
from flask import url_for


# def idparametrize(name, values, fixture=False):
#     return pytest.mark.parametrize(name, values, ids=map(repr, values), indirect=fixture)


@pytest.mark.parametrize('urls', ['index', 'chu', 'test1', 'test2', 'test3', 'test4'])
# @idparametrize('urls', ['test1', 'test2'])
def test_page_urls(urls, client):
    response = client.get(url_for(urls), follow_redirects=True)
    assert response.status_code==200