export const API_BASE = "http://127.0.0.1:8000";

export async function shortenUrl(url: string): Promise<string> {
  const res = await fetch(`${API_BASE}/shorten`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    throw new Error(`API_ERROR_${res.status}`);
  }

  const data = await res.json();
  return data.short_url;
}

export async function getStats(code: string): Promise<Record<string, any>> {
  const res = await fetch(`${API_BASE}/${code}/stats`);

  if (!res.ok) {
    throw new Error("Stats not found");
  }

  return await res.json();
}
