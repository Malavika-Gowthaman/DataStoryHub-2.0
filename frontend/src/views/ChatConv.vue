<template>
  <div
    class="p-5 md:p-10 w-full flex flex-col gap-6"
    v-for="(chat, i) in chatStore.currentChatsInContext?.messages"
    :key="i"
  >
    <p
      class="text-sm md:text-base md:w-[520px] bg-customBgPurple p-5 rounded-xl ml-auto"
    >
      {{ chat.question }}
    </p>

    <div class="flex flex-col items-center">
      <div class="md:w-[720px] flex flex-col gap-10">
        <!-- Table -->
        <div v-if="chat.results.length" class="flex flex-col gap-3">
          <h3 class="text-2xl font-bold">Table</h3>
          <div class="flex justify-end">
            <Button
              icon="pi pi-download"
              @click="exportData(i)"
              raised
              rounded
              aria-label="Export Data"
            />

            <Button
              icon="pi pi-copy"
              @click="copyToClipboard(i)"
              raised
              rounded
              aria-label="Copy Data"
            />
          </div>

          <div class="max-h-[450px] overflow-y-scroll">
            <DataTable
              :ref="setItemRef(i)"
              :pt="{
                bodyRow: '!bg-transparent !text-white',
              }"
              class="chat-table text-xs w-[350px] md:w-full"
              :value="chat.results"
              showGridlines
            >
              <Column
                v-for="item in Object.keys(chat.results[0])"
                :field="item"
                :header="item.toUpperCase()"
                :style="{
                  width: 100 / Object.keys(chat.results[0]).length + '%',
                }"
              ></Column>
            </DataTable>
          </div>
        </div>

        <!-- Summary -->
        <div class="flex flex-col gap-3">
          <h3 class="text-2xl font-bold">Summary</h3>
          <pre class="whitespace-pre-wrap text-gray-200">{{
            chat.summary
          }}</pre>
        </div>

        <!-- Follow-Up questions -->
        <div class="flex flex-col gap-3">
          <h3 class="text-xl font-bold">Follow-up Questions</h3>
          <ol class="text-base text-gray-200 space-y-3.5" type="1">
            <li v-for="(question, i) in chat.followup_questions" :key="i">
              {{ question }}
            </li>
          </ol>
        </div>
      </div>
    </div>
  </div>

  <!-- Skeleton Loader -->
  <div
    v-if="showSkeletonLoader()"
    class="flex flex-col gap-6"
    :class="!chatStore.currentChatsInContext?.messages.length ? 'mt-8' : ''"
  >
    <p
      class="text-sm md:text-base md:w-[520px] bg-customBgPurple p-5 mr-10 rounded-xl ml-auto"
    >
      {{ chatStore.currentQuestionInProgress }}
    </p>
    <div class="w-full flex items-center justify-center">
      <ChatConvSkelton class="w-[720px]" scroll-into-view>
        <template #topContent> </template>
      </ChatConvSkelton>
    </div>
  </div>
  <Home
    v-else-if="
      !showSkeletonLoader() && !chatStore.currentChatsInContext?.messages.length
    "
  />
</template>

<script setup lang="ts">
import { ref, watch, type Ref } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import { useRoute } from "vue-router";
import ChatConvSkelton from "@src/components/ChatConvSkelton.vue";
import { useChatStore } from "@src/store/chats";
import { Button, useToast } from "primevue";
import Home from "./Home.vue";

const route = useRoute();
const chatStore = useChatStore();
const tableRefs: Ref<(InstanceType<typeof DataTable> | null)[]> = ref([]);
const toast = useToast();

const showSkeletonLoader = () => {
  if (chatStore.fetchingDataFor["askQuestion"]) return true;
  else if (chatStore.fetchingDataFor["fetchChatInContext"]) return true;
  return false;
};

function copyToClipboard(index: number) {
  const tableData =
    chatStore.currentChatsInContext?.messages[index].results || [];

  // Prepare the data as a CSV string
  const headers = Object.keys(tableData[0]); // Get table headers
  const csvData = [
    headers.join(","), // Header row
    ...tableData.map((row) => headers.map((header) => row[header]).join(",")), // Data rows
  ].join("\n");

  // Copy to the clipboard using the Clipboard API
  navigator.clipboard
    .writeText(csvData)
    .then(() => {
      toast.add({
        severity: "success",
        summary: "Data copied to clipboard!",
        life: 1000,
      });
    })
    .catch((error) => {
      console.error("Failed to copy data:", error);
      toast.add({
        severity: "error",
        summary: "Failed to copy data to clipboard",
        life: 1000,
      });
    });
}

function setItemRef(index: number) {
  return (el: InstanceType<typeof DataTable> | null) => {
    tableRefs.value[index] = el;
    return undefined;
  };
}

const exportData = (index: number): void => {
  tableRefs.value[index]?.exportCSV();
  toast.add({
    severity: "success",
    summary: "Download Success",
    life: 1000,
  });
};

watch(
  route,
  async () => {
    try {
      const chatId = route.params.id;
      await chatStore.fetchChatInContext(String(chatId));
    } catch (error) {
      console.log(error);
    }
  },
  { immediate: true }
);
</script>

<style scoped>
ol {
  list-style-type: decimal;
  padding-left: 15px;
}

li {
  font-size: 16px;
  line-height: 1.5;
}
</style>

<style>
.chat-table .p-datatable-header-cell {
  background-color: transparent;
  color: white;
  font-weight: bolder;
}
</style>
