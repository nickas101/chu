from flask import url_for


def test_page_urls(client):
    # response = test_client.get(url_for('test1'), follow_redirects=True)
    response = client.get(url_for('test2'), follow_redirects=True)
    # response = client.get('http://localhost:5000/chu/test1')
    # response = client.get('/chu/test2')
    assert response.status_code==200