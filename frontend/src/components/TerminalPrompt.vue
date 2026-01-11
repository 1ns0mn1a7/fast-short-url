<template>
  <div class="space-y-3">
    <!-- Prompt -->
    <div>
      <span>C:\FAST_SHORT_URL&gt;</span>
    </div>

    <!-- Input line -->
    <div class="flex items-center gap-2">
      <span>ENTER URL:</span>
      <input
        v-model="url"
        type="text"
        class="bg-black border-b border-green outline-none text-green flex-1"
        placeholder="https://example.com"
      />
    </div>

    <!-- Action -->
    <button
      @click="run"
      class="mt-2 border border-green px-4 py-1 hover:bg-green hover:text-black"
    >
      EXECUTE
    </button>

    <!-- Result -->
    <div v-if="result" class="pt-2">RESULT: {{ result }}</div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

const url = ref("");
const result = ref<string | null>(null);

function run() {
  if (!url.value) return;
  result.value = "https://fsu/abc123";
}
</script>
