from app.utils import generate_short_url


class URLShortenerService:
    def __init__(self, storage: dict):
        self.storage = storage

    def create_short_url(self, original_url: str) -> str:
        while True:
            code = generate_short_url()
            if code not in self.storage:
                break

        self.storage[code] = {"url": original_url, "clicks": 0}
        return code

    def get_original_url(self, code: str) -> str | None:
        link = self.storage.get(code)
        if not link:
            return None

        link["clicks"] += 1
        return link["url"]

    def get_stats(self, code: str) -> dict | None:
        link = self.storage.get(code)
        if not link:
            return None

        return {"clicks": link["clicks"]}
