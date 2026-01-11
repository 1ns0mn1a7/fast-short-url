import { ref, onMounted } from "vue";

const STORAGE_KEY = "terminal_history";

export function useHistory() {
  const history = ref<string[]>([]);
  const historyIndex = ref<number | null>(null);

  onMounted(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        history.value = JSON.parse(saved);
      } catch {
        /* ignore */
      }
    }
  });

  function push(cmd: string) {
    if (!cmd.trim()) return;

    history.value.push(cmd);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history.value));
    historyIndex.value = null;
  }

  function prev(): string | null {
    if (!history.value.length) return null;

    if (historyIndex.value === null) {
      historyIndex.value = history.value.length - 1;
    } else if (historyIndex.value > 0) {
      historyIndex.value--;
    }

    return history.value[historyIndex.value];
  }

  function next(): string | null {
    if (historyIndex.value === null) return null;

    if (historyIndex.value < history.value.length - 1) {
      historyIndex.value++;
      return history.value[historyIndex.value];
    }

    historyIndex.value = null;
    return "";
  }

  function resetIndex() {
    historyIndex.value = null;
  }

  return {
    push,
    prev,
    next,
    resetIndex,
  };
}
