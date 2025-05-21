<template>
  <div :class="props.layoutStyle">
    <slot></slot>
    <div v-if="$slots.title">
      <h2 :class="props.titleStyle">
        <slot name="title"></slot>
      </h2>
    </div>
    <div v-if="$slots.subtitle">
      <slot name="subtitle" />
    </div>
    <div v-if="$slots.content">
      <p :class="props.contentStyle">
        <slot name="content" />
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  layoutStyle: {
    type: String,
    required: false,
    default:
      "bg-customBgPurple  rounded-lg p-4 hover:shadow-xl transition-shadow duration-300 cursor-pointer",
  },
  titleStyle: {
    type: String,
    required: false,
    default: "text-lg font-semibold text-purple-300 mb-2",
  },
  contentStyle: {
    type: String,
    required: false,
    default: "text-sm text-gray-300",
  },
});
</script>
