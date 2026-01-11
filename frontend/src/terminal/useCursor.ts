import { ref, onMounted, onUnmounted } from "vue";

export function useCursor(interval = 500) {
  const cursorVisible = ref(true);
  let timer: number | undefined;

  onMounted(() => {
    timer = window.setInterval(() => {
      cursorVisible.value = !cursorVisible.value;
    }, interval);
  });

  onUnmounted(() => {
    if (timer) {
      clearInterval(timer);
    }
  });

  return {
    cursorVisible,
  };
}
