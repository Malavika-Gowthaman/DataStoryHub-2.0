<template>
  <div class="flex items-start rounded-lg">
    <InputText
      type="text"
      v-model="model"
      class="w-full h-full !bg-transparent"
      :class="props.customClass"
      :placeholder="props.placeHolder"
      ref="myInput"
    />
    <slot name="content"></slot>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, useTemplateRef, watch } from "vue";
import InputText from "primevue/inputtext";

const props = defineProps({
  placeHolder: { type: String },
  autoFocus: { type: Boolean, default: false },
  value: { type: String, default: "" },
  customClass: { type: String },
});

const emit = defineEmits<{
  (e: "onValueChange", value: string): void;
}>();

const model = defineModel({ required: true, default: "" });

const myInput = ref<HTMLInputElement | null>(null);
const myInputRef = useTemplateRef("myInput");

onMounted(() => {
  if (props.autoFocus && myInput.value) {
    myInputRef.value?.$el.focus();
  }
});

watch(model, () => {
  emit("onValueChange", model.value);
});
</script>

<style scoped></style>
