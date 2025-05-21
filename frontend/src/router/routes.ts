import ChatConv from "../views/ChatConv.vue";
import HomeView from "../views/Home.vue";
import Login from "../views/Login.vue";

const routes = [
  { path: "/", component: HomeView, name: "Home" },
  { path: "/chat/:id", component: ChatConv, name: "Chat Conversation" },
  { path: "/login", component: Login, name: "Login" },
  { path: "/signup", component: Login, name: "SignUp" },
];

export default routes;
