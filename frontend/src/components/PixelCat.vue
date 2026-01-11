<template>
  <div
    class="pixel-cat"
    :style="{
      transform: `translateX(${x}px) scaleX(${direction === 'left' ? -1 : 1})`,
    }"
  >
    <pre>{{ frame }}</pre>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";

const frames = [
  ` /\\_/\\
( o.o )
 > ^ <`,
  ` /\\_/\\
( o.o )
  >^<`,
];

const frame = ref(frames[0]);
let frameIndex = 0;

const x = ref(0);
const direction = ref<"right" | "left">("right");

const speed = 0.25;
let lastFrameSwitch = 0;

function animate(time: number) {
  // движение
  x.value += direction.value === "right" ? speed : -speed;

  const maxX = window.innerWidth - 80;
  if (x.value > maxX) direction.value = "left";
  if (x.value < 0) direction.value = "right";

  // смена кадра
  if (time - lastFrameSwitch > 400) {
    frameIndex = (frameIndex + 1) % frames.length;
    frame.value = frames[frameIndex];
    lastFrameSwitch = time;
  }

  requestAnimationFrame(animate);
}

onMounted(() => {
  requestAnimationFrame(animate);
});
</script>

<style scoped>
.pixel-cat {
  position: fixed;
  bottom: 6px;
  white-space: pre;
  font-family: "VT323", monospace;
  font-size: 14px;
  line-height: 1;
  color: #22c55e;
  pointer-events: none;
  user-select: none;
  will-change: transform;
}
</style>
