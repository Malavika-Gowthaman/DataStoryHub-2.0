<template>
  <Card
    @click.stop="onClick"
    class="border border-gray-400 rounded-md !p-3 hover:cursor-pointer"
  >
    <template #content>
      <div class="flex items-center gap-2">
        <i class="pi pi-plus"></i> New Chat
      </div></template
    >
  </Card>
</template>

<script lang="ts" setup>
import { useChatStore } from "@src/store/chats";
import Card from "./base/BaseCard.vue";

const chatStore = useChatStore();

const onClick = () => {
  chatStore.createChat();
};
</script>
