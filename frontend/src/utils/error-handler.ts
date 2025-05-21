import router from "@src/router";
import axios from "axios";
import { type ToastServiceMethods } from "primevue";

export const handleErrors = (
  err: unknown,
  toast: ToastServiceMethods | null = null
) => {
  console.log("in handleErrors =>", err);
  if (axios.isAxiosError(err)) {
    const status = err.response?.status;
    const data = err.response?.data;
    switch (status) {
      case 401: {
        if (toast) {
          toast.add({
            severity: "error",
            summary: "Login Error",
            detail: data.detail,
            life: 2000,
          });
        }
        localStorage.removeItem("token");
        router.push({ name: "Login" });
        break;
      }

      case 404: {
        if (toast) {
          toast.add({
            severity: "error",
            detail: data.detail,
            life: 2000,
          });
        }
        break;
      }

      case 400: {
        if (toast) {
          toast.add({
            severity: "error",
            detail: data.detail,
            life: 2000,
          });
        }
        break;
      }
    }
  }
  return err;
};
