<template>
  <div ref="myInput" class="flex items-start rounded-lg">
    <Password
      v-model="model"
      class="w-full h-full !bg-transparent !text-white"
      :input-class="props.customClass"
      :placeholder="props.placeHolder"
      :toggle-mask="toggleMask"
    />
    <slot name="content"></slot>
  </div>
</template>

<script lang="ts" setup>
import { Password } from "primevue";
import { onMounted, ref } from "vue";

const props = defineProps({
  placeHolder: { type: String },
  autoFocus: { type: Boolean, default: false },
  value: { type: String, default: "" },
  customClass: { type: String },
  toggleMask: { type: Boolean, default: true },
});

const model = defineModel({ required: true, default: "" });

const myInput = ref<HTMLInputElement | null>(null);

onMounted(() => {
  if (props.autoFocus && myInput.value) {
    const inputElement = myInput.value.querySelector("input");
    if (inputElement) inputElement.focus();
  }
});
</script>

<style scoped></style>
