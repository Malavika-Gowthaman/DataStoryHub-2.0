import api from "@src/api";
import type { IChatConvResponse, IGetChatConvResponse } from "@src/api/chat";
import { apiConstants } from "@src/api/constants";
import axiosInstance from "@src/plugins/axios";
import { handleErrors } from "@src/utils/error-handler";
import { defineStore } from "pinia";
import { useToast } from "primevue";
import { ref } from "vue";

export const useChatStore = defineStore("chats", () => {
  const currentChatsInContext = ref<IGetChatConvResponse | null>(null);
  const fetchingDataFor = ref<{ [key: string]: boolean }>({});
  const currentQuestionInProgress = ref<string | null>(null);
  const chatConvHistory = ref<IChatConvResponse[] | null>(null);
  const chatConvSearchResult = ref<IChatConvResponse[] | null>(null);
  const toast = useToast();

  const setFetchingDataFor = (name: string) => {
    if (fetchingDataFor.value[name]) delete fetchingDataFor.value[name];
    else fetchingDataFor.value[name] = true;
  };

  // Chats
  const getChatConvHistory = (data?: unknown, callBack?: () => void) => {
    setFetchingDataFor("getChatConvHistory");
    const promise = api.chats.getChatConvHistory().then((result) => {
      chatConvHistory.value = result.data;
      return result;
    });
    if (callBack) {
      promise.then(callBack);
    }
    promise.catch(handleErrors);
    promise.finally(() => {
      setFetchingDataFor("getChatConvHistory");
    });
  };

  const createChat = async (callBack?: (data: unknown) => void) => {
    setFetchingDataFor("createChat");
    const chatPromise = api.chats.createChat().then((data) => {
      setFetchingDataFor("createChat");
      return data;
    });
    if (callBack) chatPromise.then(callBack);
    else chatPromise.then(getChatConvHistory);

    chatPromise.catch(handleErrors);
  };

  const deleteChat = async (chat_id: string, callBack?: () => void) => {
    setFetchingDataFor("deleteChat");
    api.chats
      .deleteChatConv(chat_id)
      .then(() => setFetchingDataFor("deleteChat"))
      .finally(() => {
        getChatConvHistory();
        if (callBack) callBack();
      })
      .catch(handleErrors);
  };

  const editChatTitle = async (chat_id: string, title: string) => {
    setFetchingDataFor("editChatTitle");
    api.chats
      .editChatTitle(chat_id, title)
      .then(() => setFetchingDataFor("editChatTitle"))
      .then(getChatConvHistory)
      .catch(handleErrors);
  };

  // ChatConv Screen
  const fetchChatInContext = async (chatId: string) => {
    setFetchingDataFor("fetchChatInContext");
    currentChatsInContext.value = null;
    axiosInstance
      .get<IGetChatConvResponse>(`${apiConstants.chatConv}/${chatId}`)
      .then((response) => {
        currentChatsInContext.value = response.data;
      })
      .catch(handleErrors)
      .finally(() => setFetchingDataFor("fetchChatInContext"));
  };

  const askQuestion = async (chat_id: string, question: string) => {
    setFetchingDataFor("askQuestion");
    currentQuestionInProgress.value = question;
    api.chats
      .askQuestion(chat_id, question)
      .then((response) => {
        currentChatsInContext.value?.messages.push(response.data);
      })
      .catch((err) => handleErrors(err, toast))
      .finally(() => {
        setFetchingDataFor("askQuestion");
        currentQuestionInProgress.value = null;
      });
  };
  return {
    currentChatsInContext,
    fetchingDataFor,
    fetchChatInContext,
    askQuestion,
    currentQuestionInProgress,
    getChatConvHistory,
    chatConvHistory,
    deleteChat,
    createChat,
    editChatTitle,
    chatConvSearchResult,
  };
});
