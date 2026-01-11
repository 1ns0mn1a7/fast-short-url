<template>
  <TerminalView
    v-model:terminalRef="terminalRef"
    v-model:hiddenInput="hiddenInput"
    :lines="lines"
    :input="input"
    :prompt="prompt"
    :cursorVisible="cursorVisible"
    @key="onKey"
    @focus="focusInput"
    @copy="copyLink"
  >
    <PixelCat />
  </TerminalView>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import PixelCat from "./components/PixelCat.vue";
import { sleep } from "@/terminal/helpers";
import { useCursor } from "@/terminal/useCursor";
import { useHistory } from "@/terminal/useHistory";
import { useTerminalLines } from "@/terminal/useTerminalLines";
import { createCommandHandler } from "@/terminal/commands";
import { useTyping } from "@/terminal/useTyping";
import TerminalView from "@/components/TerminalView.vue";

const { cursorVisible } = useCursor();
const history = useHistory();
const terminalRef = ref<HTMLDivElement | null>(null);

const { lines, print, ok, error, clear } = useTerminalLines(terminalRef);

const { typeLine, loadingDots } = useTyping({ lines });

const { handleCommand } = createCommandHandler({
  print,
  ok,
  error,
  clear,
  typeLine,
  loadingDots,
  setBusy: (v: boolean) => (busy.value = v),
});

const booting = ref(true);
const prompt = "C:\\> ";
const input = ref("");
const hiddenInput = ref<HTMLInputElement | null>(null);
const busy = ref(false);

function copyLink(line: { value: string; copied?: boolean }) {
  navigator.clipboard.writeText(line.value);

  line.copied = true;

  setTimeout(() => {
    line.copied = false;
  }, 700);
}

async function startBoot() {
  print("Initializing...");
  await sleep(400);
  ok("Ready.");
  print("Type 'help' to get started");
  print("");
  booting.value = false;
}

function handlePaste(e: KeyboardEvent): boolean {
  const isPaste = (e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "v";

  if (!isPaste) return false;

  e.preventDefault();

  navigator.clipboard
    .readText()
    .then((text) => {
      input.value += text;
    })
    .catch(() => {
      /* ignore */
    });

  return true;
}

function focusInput() {
  hiddenInput.value?.focus();
}

function onKey(e: KeyboardEvent) {
  if (booting.value) return;

  if (handlePaste(e)) {
    return;
  }

  if (booting.value || busy.value) return;

  // HISTORY UP
  if (e.key === "ArrowUp") {
    e.preventDefault();
    const prev = history.prev();

    if (prev !== null) input.value = prev;
    return;
  }

  // HISTORY DOWN
  if (e.key === "ArrowDown") {
    e.preventDefault();
    const next = history.next();

    if (next !== null) input.value = next;
    return;
  }

  if (e.key === "Backspace") {
    input.value = input.value.slice(0, -1);
    return;
  }

  if (e.key === "Enter") {
    print(prompt + input.value);

    history.push(input.value);

    handleCommand(input.value);
    input.value = "";
    return;
  }

  if (e.key.length === 1) {
    input.value += e.key;
  }
}

onMounted(async () => {
  await startBoot();
  await sleep(200);
  hiddenInput.value?.focus();
});
</script>
