import type { CommandSpec } from "@/types/terminal";

export const commandSpecs: Record<string, CommandSpec> = {
  shorten: {
    usage: "shorten <url>",
    example: "shorten https://example.com",
    minArgs: 1,
  },
  stats: {
    usage: "stats <code | url>",
    example: "stats abc123",
    minArgs: 1,
  },
  about: { usage: "about" },
  clear: { usage: "clear" },
};
