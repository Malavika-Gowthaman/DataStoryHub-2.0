<template>
  <main
    class="text-white bg-linear-to-b from-customPurple via-gray-900 to-black relative"
  >
    <!-- Only for the Login and SignUp page -->
    <RouterView v-if="isLoginOrSignUp" />

    <div v-else>
      <!-- Hamburger Menu (Mobile) -->
      <i
        v-if="isMobile()"
        class="pi pi-bars hover:cursor-pointer m-5"
        @click="isDrawerVisible = true"
      ></i>

      <!-- For Mobile Drawer -->
      <Drawer
        class="!bg-linear-to-b from-customPurple via-gray-900 to-black relative max-w-[250px] !border-none"
        v-model:visible="isDrawerVisible"
      >
        <template #container>
          <div class="flex items-center bg-transparent justify-end">
            <i
              v-if="isMobile()"
              class="pi pi-times hover:cursor-pointer m-5"
              @click="isDrawerVisible = false"
            ></i>
          </div>
          <SidePane class="w-full"> </SidePane>
        </template>
      </Drawer>

      <!-- Main -->
      <div class="flex max-h-screen">
        <!-- Side Pane -->
        <SidePane
          class="max-w-[250px] border-r-1 border-r-gray-400"
          v-if="!isMobile()"
        />
        <div class="w-full">
          <div
            class="h-[calc(100vh-11.4rem)] lg:h-[calc(100vh-8rem)] overflow-y-scroll"
          >
            <RouterView />
          </div>

          <!-- Question TextArea -->
          <div class="md:px-15 mx-3 lg:mx-auto lg:w-2/3 py-4">
            <BaseTextArea
              class="bg-customBgPurple h-24 p-2"
              v-model="askText"
              custom-class="!border-none !text-white outline-none"
              placeholder="Ask me anything..."
              :onEnter="handleOnEnter"
            >
              <template #content>
                <VoiceInput
                  ref="voiceInputRef"
                  @update:value="(value) => (askText = value)"
                  @submit="handleQuestion(askText)"
                  :show-mic-icon="true"
                  :show-send-icon="true"
                />
              </template>
            </BaseTextArea>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup lang="ts">
import { computed, ref } from "vue";
import SidePane from "../../components/SidePane.vue";
import Drawer from "primevue/drawer";
import VoiceInput from "../../components/VoiceInput.vue";
import { useRoute, useRouter } from "vue-router";
import BaseTextArea from "../../components/base/BaseTextArea.vue";
import { useChatStore } from "@src/store/chats";

const askText = ref();
const isDrawerVisible = ref(false);
const route = useRoute();
const router = useRouter();
const chatStore = useChatStore();
const voiceInputRef = ref();

const isMobile = () => {
  return window.innerWidth < 1024;
};

const handleOnEnter = () => {
  !voiceInputRef.value.isRecording && handleQuestion(askText.value);
};

const paths = ["/login", "/signup"];
const isLoginOrSignUp = computed(() => paths.includes(route.fullPath));

const handleQuestion = async (question: string) => {
  if (route.name === "Home") {
    const callBack = (data: unknown) => {
      const resultedData = data as { data: { chat_id: string } };
      router.push({
        name: "Chat Conversation",
        params: {
          id: resultedData.data.chat_id,
        },
      });

      chatStore.getChatConvHistory(null, () => {
        chatStore.askQuestion(resultedData.data.chat_id, question);
      });
    };
    chatStore.createChat(callBack);
  } else {
    chatStore.askQuestion(String(route.params.id), question);
  }
  askText.value = "";
};
</script>
