import axiosInstance from "@src/plugins/axios";
import { apiConstants } from "./constants";

export interface IChatConvResponse {
  chat_id: string;
  title: string | null;
}

export interface IGetChatConvResponse extends IChatConvResponse {
  messages: {
    question: string;
    sql_query: string;
    execution_time: number;
    results: { [key: string]: string | number }[];
    summary: string;
    followup_questions: string[];
  }[];
}

const getChatConvHistory = async () => {
  return axiosInstance.get<IChatConvResponse[]>(apiConstants.chatConv);
};

const getChatConv = async (chatId: string) => {
  return axiosInstance.get<IGetChatConvResponse>(
    `${apiConstants.chatConv}/${chatId}`
  );
};

const createChat = async () => {
  return axiosInstance.post<{ chat_id: string }>(apiConstants.chatConv);
};

const deleteChatConv = async (chat_id: string) => {
  return axiosInstance.delete(`${apiConstants.chatConv}/${chat_id}`);
};

const askQuestion = async (chat_id: string, question: string) => {
  return axiosInstance.post<IGetChatConvResponse["messages"][0]>(
    apiConstants.ask,
    {
      chat_id,
      question,
    }
  );
};

const editChatTitle = async (chat_id: string, title: string) => {
  return axiosInstance.patch<{ msg: string }>(
    `${apiConstants.chatConv}/${chat_id}/title`,
    {
      title,
    }
  );
};

export class ChatsApi {
  getChatConvHistory = getChatConvHistory;
  getChatConv = getChatConv;
  askQuestion = askQuestion;
  deleteChatConv = deleteChatConv;
  createChat = createChat;
  editChatTitle = editChatTitle;
}
