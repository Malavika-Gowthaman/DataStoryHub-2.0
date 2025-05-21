<template>
  <slot :typedValue="localValue"></slot>
</template>

<script lang="ts" setup>
import { onMounted, ref, watch } from "vue";
import { useAutoTypeCompStore } from "../store/autoTypeComp";

const props = defineProps({
  value: {
    type: String,
    required: true,
  },
  speed: {
    type: Number,
    default: 100,
  },
  startNow: {
    type: Boolean,
    default: false,
  },
  startNextOnceDone: {
    type: Boolean,
    default: false,
  },
});

const emit = defineEmits<{
  (e: "done:typed"): void;
}>();

const autoTypeCompStore = useAutoTypeCompStore();

const valueCpy = props.value.split("");
const localValue = ref("");

const registerInterval = () => {
  let interval = setInterval(() => {
    if (!valueCpy.length) {
      emit("done:typed");
      if (props.startNextOnceDone) autoTypeCompStore.startNextAutoTypeComp();
      return clearInterval(interval);
    }
    localValue.value = localValue.value + valueCpy.shift();
  }, props.speed);
};

onMounted(() => {
  autoTypeCompStore.stackAutotypedCompoenents.push({
    key: props.value,
    start: registerInterval,
  });
});

watch(
  [props],
  () => {
    if (props.startNow) registerInterval();
  },

  {
    immediate: true,
  }
);
</script>
