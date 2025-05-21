<template>
  <div>
    <!-- New Conversation -->
    <div
      v-if="!showSkeletonLoader()"
      class="flex flex-col w-full gap-4 pr-4 lg:pr-1"
    >
      <Card
        v-for="(conv, i) in chatStore.chatConvSearchResult ||
        chatStore.chatConvHistory"
        :key="i"
        class="w-full h-10 rounded-md font-medium"
        :class="route.params.id === conv.chat_id ? 'bg-customPurpleCard' : ''"
        @click="gotoChat(conv.chat_id)"
      >
        <div class="flex gap-2 items-center h-full">
          <BaseInput
            v-if="currentEditTileId && currentEditTileId === conv.chat_id"
            custom-class="!border-none !text-xs !text-white"
            auto-focus
            v-model="tempMessageTitle"
          />

          <div v-else class="flex items-center gap-2">
            <i class="pi pi-comment text-white"></i>
            <p class="text-xs h-6 text-white w-full flex items-center">
              {{
                `${conv.title?.substring(0, 15) || "New Convsation"} ${
                  conv.title ? "..." : ""
                }`
              }}
            </p>
          </div>

          <!-- Edit, Delete -->
          <div class="ml-auto">
            <div v-if="!currentEditTileId" class="flex gap-3 text-gray-300">
              <i
                @click.stop="onEdit(conv.chat_id, conv.title)"
                class="pi pi-pencil hover:text-white !text-sm"
              ></i>
              <i
                @click.stop="onDelete(conv.chat_id, i)"
                class="pi pi-trash hover:text-white !text-sm"
              ></i>
            </div>

            <!-- Save and Cancel -->
            <div
              v-if="currentEditTileId && currentEditTileId === conv.chat_id"
              class="flex gap-3 text-gray-300"
            >
              <i
                @click.stop="onSave(conv.chat_id)"
                class="pi pi-check hover:text-white !text-sm"
              ></i>
              <i
                class="pi pi-times hover:text-white !text-sm"
                @click.stop="onCancel"
              ></i>
            </div>
          </div>
        </div>
      </Card>
    </div>

    <!-- Skeleton loaders -->
    <div v-if="showSkeletonLoader()" class="flex flex-col gap-6">
      <BaseSkeleton
        v-for="i in 11"
        :key="i"
        shape="rectangle"
        class="!bg-customBgPurple rounded"
      ></BaseSkeleton>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import Card from "./base/BaseCard.vue";
import BaseInput from "./base/BaseInput.vue";
import { useRoute, useRouter } from "vue-router";
import { useChatStore } from "@src/store/chats";
import BaseSkeleton from "./base/BaseSkeleton.vue";

// Variables
const tempMessageTitle = ref("");
const router = useRouter();
const chatStore = useChatStore();
const currentEditTileId = ref<string | null>(null);
const route = useRoute();

// States
const clearTempMessageTitle = () => (tempMessageTitle.value = "");

// Methods
const onEdit = (chat_id: string, previousTitle: string | null) => {
  currentEditTileId.value = chat_id;
  tempMessageTitle.value = previousTitle || "";
};

const onCancel = () => {
  currentEditTileId.value = null;
  clearTempMessageTitle();
};

const onSave = (chat_id: string) => {
  chatStore.editChatTitle(chat_id, tempMessageTitle.value);
  clearTempMessageTitle();
  currentEditTileId.value = null;
};

const onDelete = (chat_id: string, index: number) => {
  const callBack = () => {
    if (chatStore.chatConvHistory && chatStore.chatConvHistory?.length > 1) {
      const chat =
        index === chatStore.chatConvHistory?.length - 1
          ? chatStore.chatConvHistory[index - 1]
          : chatStore.chatConvHistory[index + 1];
      router.replace({
        name: "Chat Conversation",
        params: { id: chat.chat_id },
      });
    } else {
      router.replace({
        name: "Home",
      });
    }
  };
  chatStore.deleteChat(chat_id, callBack);
};

const gotoChat = (chatId: string) => {
  router.push({
    name: "Chat Conversation",
    params: {
      id: chatId,
    },
  });
};

const showSkeletonLoader = () => {
  if (chatStore.fetchingDataFor["editChatTitle"]) return true;
  else if (chatStore.fetchingDataFor["deleteChat"]) return true;
  else if (chatStore.fetchingDataFor["getChatConvHistory"]) return true;
  else if (chatStore.fetchingDataFor["createChat"]) return true;
  return false;
};

onMounted(() => {
  if (!chatStore.chatConvHistory) {
    chatStore.getChatConvHistory();
  }
});

watch(route, () => {
  currentEditTileId.value = null;
});
</script>
