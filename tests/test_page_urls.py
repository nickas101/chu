from flask import url_for


def test_page_urls(client):
    # Visit home page
    response = client.get(url_for('test1'), follow_redirects=True)
    assert response.status_code==200