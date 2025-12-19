def test_health_route(client, monkeypatch):
    ## Setup
    monkeypatch.setattr(
        "subprocess.check_output",
        lambda *args, **kwargs: b"1234abc" if "git" in args[0] else b"1.0.0",
    )

    ## Test
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()

    assert data["status"] == "healthy"
    assert "version" in data
    assert "commit_hash" in data
