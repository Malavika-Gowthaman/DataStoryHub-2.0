<template>
  <div class="flex flex-col items-end">
    <div
      v-if="showMicIcon"
      :class="{ 'flex items-center px-2 bg-white rounded-4xl': isRecording }"
    >
      <button class="p-2 text-gray-400 hover:cursor-pointer" @click="toggleMic">
        <i class="pi pi-microphone"></i>
      </button>
      <VoiceAnimation :show-voice="isRecording" />
    </div>

    <button
      @click="
        () => {
          sr.stop();
          emit('submit');
        }
      "
      v-if="showSendIcon"
      class="p-2 text-gray-400 hover:cursor-pointer"
    >
      <i class="pi pi-send"></i>
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from "vue";
import VoiceAnimation from "./VoiceAnimation.vue";

const props = defineProps({
  showMicIcon: { type: Boolean, default: false },
  showSendIcon: { type: Boolean, default: false },
  value: { type: String, default: "" },
});

const emit = defineEmits<{
  (e: "update:value", value: string): void;
  (e: "submit"): void;
}>();

const transcript = ref("");
const isRecording = ref(false);
const localState = ref(props.value);

// Speech Recognition Setup
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const sr = new Recognition();
sr.continuous = true;
sr.interimResults = true;

sr.onstart = () => (isRecording.value = true);
sr.onend = () => (isRecording.value = false);
sr.onresult = (evt: any) => {
  transcript.value = Array.from(evt.results)
    .map((result: any) => result[0].transcript)
    .join("");
};

// Start/Stop Microphone
const toggleMic = () => {
  isRecording.value ? sr.stop() : sr.start();
};

defineExpose({
  stopMic: sr.stop,
  startMic: sr.start,
  isRecording,
});

watch(transcript, () => {
  localState.value = transcript.value;
  emit("update:value", transcript.value);
});
</script>
