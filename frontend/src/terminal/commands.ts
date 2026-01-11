import { commandSpecs } from "@/terminal/commandSpecs";
import { helpMap } from "@/terminal/helpMap";
import { extractCode } from "@/terminal/helpers";
import { shortenUrl, API_BASE, getStats } from "@/api";

type Deps = {
  print: (text: string) => void;
  ok: (text: string) => void;
  error: (text: string) => void;
  clear: () => void;
  typeLine: (text: string, delay?: number) => Promise<void>;
  loadingDots: (
    text: string,
    duration?: number,
    interval?: number,
  ) => Promise<void>;
  setBusy: (v: boolean) => void;
};

export function createCommandHandler(deps: Deps) {
  const { print, ok, error, clear, typeLine, loadingDots, setBusy } = deps;

  function printUsage(cmd: string) {
    const spec = commandSpecs[cmd];
    if (!spec) return;

    print(`Usage: ${spec.usage}`);
    if (spec.example) {
      print(`Example: ${spec.example}`);
    }
    print("");
  }

  async function handleCommand(cmd: string) {
    const raw = cmd.trim();
    if (!raw) return;

    const parts = raw.split(/\s+/);
    const name = parts[0].toLowerCase();
    const args = parts.slice(1);

    const spec = commandSpecs[name];
    if (spec?.minArgs && args.length < spec.minArgs) {
      printUsage(name);
      return;
    }

    // HELP
    if (name === "help" && args.length) {
      const key = args[0];
      const info = helpMap[key];

      if (!info) {
        error(`No help for '${key}'`);
        print("");
        return;
      }

      info.forEach((line) => print(line));
      print("");
      return;
    }

    if (name === "help") {
      print("AVAILABLE COMMANDS:");
      print("");
      print("  shorten <url>   Generate short link");
      print("  stats <code>    Show link statistics");
      print("  about           Program information");
      print("  clear           Clear screen");
      print("");
      return;
    }

    // ABOUT
    if (name === "about") {
      print("FAST_SHORT_URL.EXE v0.1");
      print("Author: 1NS0MN1A7");
      print("Source:");
      print("https://github.com/1ns0mn1a7/fast-short-url");
      print("");
      return;
    }

    // CLEAR
    if (name === "clear") {
      clear();
      return;
    }

    // SHORTEN
    if (name === "shorten") {
      const url = args[0];

      setBusy(true);
      try {
        await typeLine("Generating short link...", 25);

        const shortCode = await shortenUrl(url);
        const redirectUrl = `${API_BASE}/${shortCode}`;

        await typeLine("Done.", 30);
        await typeLine(redirectUrl, 15);
      } catch {
        error("FAILED TO SHORTEN URL");
      } finally {
        setBusy(false);
        print("");
      }
      return;
    }

    // STATS
    if (name === "stats") {
      const arg = args[0];
      const { code, reason } = extractCode(arg);

      if (!code) {
        if (reason === "NO_CODE_IN_URL")
          error("URL DOES NOT CONTAIN SHORT CODE");
        else if (reason === "INVALID_URL") error("INVALID URL");
        else error("CODE REQUIRED");
        print("");
        return;
      }

      setBusy(true);
      try {
        await loadingDots(`Fetching stats for ${code} `);

        const stats = await getStats(code);

        ok(`Code: ${stats.code}`);

        if ("clicks" in stats) print(`Clicks: ${stats.clicks}`);
        if ("created_at" in stats) print(`Created: ${stats.created_at}`);
        if ("expires_at" in stats && stats.expires_at) {
          print(`Expires: ${stats.expires_at}`);
        }
      } catch {
        error("STATS NOT FOUND");
      } finally {
        setBusy(false);
        print("");
      }
      return;
    }

    // UNKNOWN
    error(`'${cmd}' is not recognized as an internal command`);
    print("");
  }

  return { handleCommand };
}
