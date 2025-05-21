<template>
  <div ref="container">
    <slot name="topContent"></slot>
    <div class="flex flex-col gap-4">
      <BaseSkeleton
        v-for="n in 5"
        :key="n"
        shape="rectangle"
        class="!bg-customBgPurple rounded"
      ></BaseSkeleton>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import BaseSkeleton from "./base/BaseSkeleton.vue";

const props = defineProps<{ scrollIntoView: boolean }>();

const container = ref<HTMLElement | null>(null);

const scrollToLast = async (): Promise<void> => {
  const lastElement = container.value?.lastElementChild as HTMLElement | null;
  if (lastElement) {
    lastElement.scrollIntoView({ behavior: "smooth" });
  }
};

onMounted(() => {
  if (props.scrollIntoView) scrollToLast();
});
</script>
