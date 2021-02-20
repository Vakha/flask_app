from shepherd import create_app


def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_overview(client):
    response = client.get('/healthcheck')
    assert response.data == b'Ok'