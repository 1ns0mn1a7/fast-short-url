import { ref, nextTick } from "vue";
import type { Line } from "@/types/terminal";

export function useTerminalLines(terminalRef: {
  value: HTMLDivElement | null;
}) {
  const lines = ref<Line[]>([]);

  function scrollToBottom() {
    nextTick(() => {
      terminalRef.value?.scrollTo({
        top: terminalRef.value.scrollHeight,
        behavior: "auto",
      });
    });
  }

  function print(text: string) {
    lines.value.push({ type: "text", value: text });
    scrollToBottom();
  }

  function ok(text: string) {
    lines.value.push({ type: "ok", value: text });
    scrollToBottom();
  }

  function error(text: string) {
    lines.value.push({ type: "error", value: text });
    scrollToBottom();
  }

  function clear() {
    lines.value.splice(0);
    scrollToBottom();
  }

  return {
    lines,
    print,
    ok,
    error,
    clear,
  };
}
