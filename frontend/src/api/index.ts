import { ChatsApi } from "./chat";
import { UserApi } from "./user";

class Api {
  user = new UserApi();
  chats = new ChatsApi();
}

export default new Api();
