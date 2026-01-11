<template>
  <div
    class="w-screen h-screen bg-black text-green-400 flex flex-col"
    style="font-family: &quot;VT323&quot;, monospace"
    @click="$emit('focus')"
  >
    <!-- BOOT HEADER -->
    <div class="px-4 pt-3 pb-2 text-xl leading-tight">
      <div>FAST_SHORT_URL.EXE v0.1</div>
      <div>(c) 2026 1NS0MN1A7. ALL RIGHTS RESERVED.</div>

      <div class="mt-1">
        SOURCE:
        <a
          href="https://github.com/1ns0mn1a7/fast-short-url"
          target="_blank"
          rel="noopener noreferrer"
          class="text-green hover:underline"
        >
          github.com/1ns0mn1a7/fast-short-url
        </a>
      </div>

      <div>&nbsp;</div>
    </div>

    <!-- TERMINAL BODY -->
    <div class="flex-1 min-h-0">
      <div
        ref="terminalRef"
        class="h-full overflow-y-auto px-4 text-xl leading-relaxed select-text relative"
      >
        <div v-for="(line, i) in lines" :key="i" class="flex ml-2">
          <!-- PREFIX -->
          <span v-if="line.type === 'ok'" class="text-green-400">
            [OK] {{ line.value }}
          </span>
          <span v-else-if="line.type === 'error'" class="text-red-400">
            [ERROR] {{ line.value }}
          </span>

          <!-- CONTENT -->
          <template v-else-if="line.type === 'text'">
            <!-- URL -->
            <template v-if="isUrl(line.value)">
              <a
                :href="line.value"
                target="_blank"
                rel="noopener noreferrer"
                class="underline text-blue-400 hover:text-blue-300 cursor-pointer"
                @click.stop
              >
                {{ line.value }}
              </a>

              <span
                class="ml-1 cursor-pointer select-none"
                @click.stop="$emit('copy', line)"
              >
                [{{ line.copied ? "copied" : "copy" }}]
              </span>
            </template>

            <!-- PLAIN TEXT -->
            <span v-else>
              {{ line.value }}
            </span>
          </template>
        </div>

        <!-- INPUT LINE -->
        <div class="flex ml-2">
          <span class="mr-2">{{ prompt }}</span>
          <span class="whitespace-pre">{{ input }}</span>
          <span>{{ cursorVisible ? "█" : " " }}</span>
        </div>
      </div>
    </div>

    <!-- HIDDEN INPUT -->
    <input
      ref="hiddenInput"
      class="absolute opacity-0 w-0 h-0"
      autocomplete="off"
      autocorrect="off"
      autocapitalize="off"
      spellcheck="false"
      @keydown="$emit('key', $event)"
    />

    <slot />
  </div>
</template>

<script setup lang="ts">
import type { Line } from "@/types/terminal";
import { isUrl } from "@/terminal/helpers";

defineProps<{
  lines: Line[];
  input: string;
  prompt: string;
  cursorVisible: boolean;
}>();

defineEmits<{
  (e: "key", ev: KeyboardEvent): void;
  (e: "focus"): void;
  (e: "copy", line: { value: string; copied?: boolean }): void;
}>();

const terminalRef = defineModel<HTMLDivElement | null>("terminalRef");
const hiddenInput = defineModel<HTMLInputElement | null>("hiddenInput");
</script>
