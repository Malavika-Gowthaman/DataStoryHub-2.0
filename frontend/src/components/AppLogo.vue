<template>
  <img
    class="w-1/3 slow-spin"
    :class="props.width"
    src="/Logo.svg"
    alt="App Logo"
  />
</template>

<script setup lang="ts">
const props = defineProps({
  width: {
    type: String,
    default: "w-1/3",
  },
});
</script>

<style scoped>
.slow-spin {
  animation: spin 10s linear infinite;
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
