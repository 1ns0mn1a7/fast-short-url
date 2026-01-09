from datetime import datetime, timedelta

from sqlalchemy import text

from app.services import URLShortenerService


TEST_URL = "https://example.com"


def test_shorten_url(client):
    response = client.post("/shorten", json={"url": TEST_URL})

    assert response.status_code == 200

    body = response.json()
    assert "short_url" in body
    assert isinstance(body["short_url"], str)
    assert len(body["short_url"]) >= 6


def test_redirect_and_clicks(client):
    create_response = client.post("/shorten", json={"url": TEST_URL})
    code = create_response.json()["short_url"]

    r1 = client.get(f"/{code}", follow_redirects=False)
    assert r1.status_code == 307

    r2 = client.get(f"/{code}", follow_redirects=False)
    assert r2.status_code == 307

    stats = client.get(f"/{code}/stats")
    assert stats.status_code == 200

    body = stats.json()
    assert body["clicks"] == 2
    assert body["code"] == code


def test_expired_link_returns_404(client, db):
    create_response = client.post("/shorten", json={"url": TEST_URL})
    code = create_response.json()["short_url"]

    db.execute(
        text("UPDATE short_links SET expires_at = :expires_at WHERE code = :code"),
        {
            "expires_at": datetime.utcnow() - timedelta(hours=1),
            "code": code,
        },
    )
    db.commit()

    response = client.get(f"/{code}", follow_redirects=False)
    assert response.status_code == 404


def test_cleanup_removes_expired_links(db):
    service = URLShortenerService(db)

    code = service.create_short_url(TEST_URL, ttl_hours=1)

    db.execute(
        text("UPDATE short_links SET expires_at = :expires_at WHERE code = :code"),
        {
            "expires_at": datetime.utcnow() - timedelta(hours=1),
            "code": code,
        },
    )
    db.commit()

    deleted = service.cleanup_expired_links()
    assert deleted == 1
