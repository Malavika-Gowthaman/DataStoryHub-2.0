import { createRouter, createWebHistory } from "vue-router";
import routes from "./routes";

const router = createRouter({
  history: createWebHistory(),
  routes,
});

const checkIsAuthenticated = () => {
  return localStorage.getItem("token");
};

const passThrowRoutes = ["Login", "SignUp"];

router.beforeEach((to, from, next) => {
  if (to.name === "Login" && checkIsAuthenticated()) next({ name: "Home" });
  if (passThrowRoutes.includes(String(to.name)) && !checkIsAuthenticated())
    next();
  else next();
});

export default router;
