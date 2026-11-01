def test_tracking_page_has_a_progressive_tracking_form(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'<form' in response.content
    assert b'method="post"' in response.content
    assert b'hx-post=' in response.content
    assert b'hx-target="#tracking-result"' in response.content
    assert b'name="tracking_id"' in response.content
