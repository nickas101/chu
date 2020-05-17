import pytest
from flask import url_for


# def idparametrize(name, values, fixture=False):
#     return pytest.mark.parametrize(name, values, ids=map(repr, values), indirect=fixture)


@pytest.mark.parametrize('urls', ['index', 'chu', 'test1', 'test2', 'test3', 'test4',
                                  'test1_result', 'test2_result', 'test3_result', 'test4_result',
                                  'test4_plot_png', 'download_plot'])
# @idparametrize('urls', ['test1', 'test2'])
def test_page_urls_get(urls, client):
    response = client.get(url_for(urls), follow_redirects=True)
    assert response.status_code == 200


@pytest.mark.parametrize('urls', ['test1', 'test2', 'test3', 'test4'])
def test_page_urls_post(urls, client):
    response = client.post(url_for(urls))
    assert response.status_code == 200
