<template>
  <div class="p-4 h-auto flex flex-col gap-4">
    <!-- Title -->

    <div class="flex items-center">
      <AppLogo />
      <h1 class="text-xl font-bold text-white">Datastory Hub</h1>
    </div>

    <div class="flex flex-col gap-4">
      <div class="flex flex-col gap-4">
        <!-- New Chat -->
        <NewChat />

        <!-- Search -->
        <BaseInput
          customClass="bg-white !text-white"
          place-holder="Search..."
          v-model="searchConv"
          @on-value-change="(value) => searchFn(() => handleSearch(value))"
        />
      </div>

      <!-- Divider -->
      <div class="border-t-1 border-gray-400"></div>

      <!-- Chat History -->
      <ConvHistory
        class="max-h-[calc(100vh-320px)] lg:max-h-[calc(100vh-260px)] overflow-y-scroll"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import BaseInput from "./base/BaseInput.vue";
import ConvHistory from "./ConvHistory.vue";
import NewChat from "./NewChat.vue";
import AppLogo from "./AppLogo.vue";
import { useChatStore } from "@src/store/chats";

const debounce = () => {
  let timeOut: number;
  return function (callBackFunc: Function, delay?: number) {
    if (timeOut) clearTimeout(timeOut);
    timeOut = setTimeout(callBackFunc, delay || 500);
  };
};

const chatStore = useChatStore();
const searchConv = ref();
const searchFn = debounce();

const handleSearch = (value: string) => {
  chatStore.chatConvSearchResult =
    chatStore.chatConvHistory?.filter((el) =>
      el.title?.toLowerCase().includes(value)
    ) || null;
};
</script>
