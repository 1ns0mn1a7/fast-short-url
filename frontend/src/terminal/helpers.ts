export function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export function isUrl(text: string): boolean {
  return /^https?:\/\/\S+$/i.test(text);
}

export function extractCode(input: string): { code?: string; reason?: string } {
  input = input.trim();

  if (!input) {
    return { reason: "EMPTY" };
  }

  // URL
  if (/^https?:\/\//i.test(input)) {
    try {
      const url = new URL(input);
      const parts = url.pathname.split("/").filter(Boolean);

      if (!parts.length) {
        return { reason: "NO_CODE_IN_URL" };
      }

      return { code: parts[parts.length - 1] };
    } catch {
      return { reason: "INVALID_URL" };
    }
  }

  // just code
  return { code: input };
}
