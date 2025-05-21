<template>
  <div class="flex items-start justify-between rounded-lg">
    <Textarea
      class="h-full w-full !bg-transparent myTextarea"
      v-bind="props"
      v-model="model"
      :class="props.customClass"
      :style="{ resize: props.resize || 'none' }"
      :placeholder="props.placeholder"
      ref="myTextarea"
      @keyup="onKeyUp"
    />
    <slot name="content"></slot>
  </div>
</template>

<script setup lang="ts">
import Textarea, { type TextareaProps } from "primevue/textarea";
import { useTemplateRef, watch } from "vue";

const model = defineModel({ required: true, default: "" });
const props = defineProps<IProps>();

const myTextarea = useTemplateRef<InstanceType<typeof Textarea> | null>(
  "myTextarea"
);

const onKeyUp = (event: { key: string }) => {
  console.log(event);
  if (event.key === "Enter" && props.onEnter) {
    props.onEnter();
  }
};

watch(model, () => {
  if (myTextarea.value) {
    myTextarea.value.$el.scrollTop = myTextarea.value.$el.scrollHeight;
  }
});
</script>

<script lang="ts">
interface IProps extends TextareaProps {
  customClass: string;
  cols?: string;
  rows?: string;
  placeholder?: string;
  resize?: boolean;
  onEnter?: () => void;
}
</script>
