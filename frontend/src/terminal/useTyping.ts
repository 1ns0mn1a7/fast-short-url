import type { Line } from "@/types/terminal";
import { sleep } from "@/terminal/helpers";

type Deps = {
  lines: { value: Line[] };
};

export function useTyping({ lines }: Deps) {
  async function typeLine(text: string, delay = 20) {
    let current = "";
    lines.value.push({ type: "text", value: "" });
    const idx = lines.value.length - 1;

    for (const ch of text) {
      current += ch;
      lines.value[idx] = { type: "text", value: current };
      await sleep(delay);
    }
  }

  async function loadingDots(text: string, duration = 1500, interval = 300) {
    const frames = [".", "..", "..."];
    let i = 0;

    lines.value.push({ type: "text", value: text });
    const idx = lines.value.length - 1;
    const start = Date.now();

    while (Date.now() - start < duration) {
      lines.value[idx] = {
        type: "text",
        value: text + frames[i % frames.length],
      };
      i++;
      await sleep(interval);
    }
  }

  return {
    typeLine,
    loadingDots,
  };
}
