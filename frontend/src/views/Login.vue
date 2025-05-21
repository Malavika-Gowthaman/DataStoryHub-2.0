<template>
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="card_style rounded-lg bg-[#1E1B3A] w-1/3">
      <div class="flex justify-center flex-col items-center p-4 pb-0">
        <!-- <img class="w-1/6" src="/Logo.svg" /> -->
        <AppLogo width="w-1/4" />
        <h1 class="text-2xl font-bold">Datastory Hub</h1>
      </div>

      <form @submit.prevent="onSubmit" class="p-5 flex flex-col gap-5">
        <div v-if="isLogin" class="flex flex-col">
          <span class="font-bold text-xl">Login</span>
          <span class="text-gray-600 font-semibold">
            Don’t have an account?
            <span class="text-blue-600 cursor-pointer" @click="onToggleUrl"
              >Sign Up</span
            >
          </span>
        </div>

        <div v-else class="flex flex-col">
          <span class="font-bold text-xl">Sign Up</span>
          <span class="text-gray-600 font-semibold">
            Already have an account?
            <span class="text-blue-600 cursor-pointer" @click="onToggleUrl"
              >Login</span
            >
          </span>
        </div>

        <!-- User Name -->
        <div v-if="!isLogin">
          <BaseInput
            v-model="form.userName"
            place-holder="User Name"
            custom-class=""
            class="h-10 bg-white focus:ring-2 focus:ring-gray-50"
          />
          <Message
            v-if="errors.userName"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ errors.userName }}
          </Message>
        </div>

        <!-- Email -->
        <div>
          <BaseInput
            v-model="form.email"
            place-holder="Email"
            custom-class=""
            class="h-10 bg-white focus:ring-2 focus:ring-gray-50"
          />
          <Message
            v-if="errors.email"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ errors.email }}
          </Message>
        </div>

        <div>
          <BasePassword
            v-model="form.password"
            place-holder="Password"
            custom-class="w-full bg-customBgPurple h-10 focus:ring-2 focus:ring-gray-50"
            :toggleMask="true"
          />
          <Message
            v-if="errors.password"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ errors.password }}
          </Message>
        </div>

        <div v-if="!isLogin">
          <BasePassword
            v-model="form.confirmPassword"
            place-holder="Confirm Password"
            custom-class="w-full bg-customBgPurple h-10 focus:ring-2 focus:ring-gray-50"
            :toggleMask="true"
          />
          <Message
            v-if="errors.confirmPassword"
            severity="error"
            size="small"
            variant="simple"
          >
            {{ errors.confirmPassword }}
          </Message>
        </div>

        <Button
          type="submit"
          label="Submit"
          class="mt-2 drop-shadow-customBgPurple !bg-blue-600"
        />
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed } from "vue";
import BaseInput from "../components/base/BaseInput.vue";
import BasePassword from "../components/base/BasePassword.vue";
import Message from "primevue/message";
import Button from "primevue/button";
import { useRoute, useRouter } from "vue-router";
import AppLogo from "../components/AppLogo.vue";
import { useToast } from "primevue";
import { handleErrors } from "../utils/error-handler";
import api from "@src/api";

const route = useRoute();
const router = useRouter();
const toast = useToast();

const onToggleUrl = (event: MouseEvent) => {
  event.preventDefault();
  const name = isLogin.value ? "SignUp" : "Login";
  router.push({ name });
};

const isLogin = computed(() => route.name === "Login");

const form = reactive({
  userName: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const errors = reactive({
  userName: "",
  email: "",
  password: "",
  confirmPassword: "",
});

const validateForm = () => {
  let isValid = true;
  errors.email = "";
  errors.password = "";
  errors.confirmPassword = "";

  if (!isLogin.value && !form.userName) {
    errors.userName = "Username is required.";
    isValid = false;
  }

  if (!form.email) {
    errors.email = "Email is required.";
    isValid = false;
  } else if (!form.email.includes("@")) {
    errors.email = "Invalid email.";
    isValid = false;
  }

  if (!form.password) {
    errors.password = "Password is required.";
    isValid = false;
  } else if (form.password.length < 3 || form.password.length > 8) {
    errors.password = "Password must be 3-8 characters.";
    isValid = false;
  }

  if (!isLogin.value && form.confirmPassword !== form.password) {
    errors.confirmPassword = "Passwords do not match.";
    isValid = false;
  }

  return isValid;
};

const loginUser = () => {
  api.user
    .loginUser({
      username: form.email,
      password: form.password,
    })
    .then(() => {
      toast.add({
        severity: "success",
        summary: "Login Success",
        detail: "",
        life: 1000,
      });
      router.push({ name: "Home" });
    })
    .catch((err) => handleErrors(err, toast));
};

const signUpUser = () => {
  api.user
    .signUpUser({
      username: form.email,
      password: form.password,
      confirm_password: form.confirmPassword,
      email: form.email,
    })
    .then(() => {
      toast.add({
        severity: "success",
        summary: "Signup Success",
        detail: "",
        life: 1000,
      });
      router.push({ name: "Login" });
    })
    .catch((err) => handleErrors(err, toast));
};

const onSubmit = async () => {
  if (validateForm()) isLogin.value ? loginUser() : signUpUser();
};
</script>

<style scoped>
.card_style {
  min-width: 370px;
  max-width: 450px;
  border: none;
  box-shadow: 0 1px 7px rgba(0, 0, 0, 0.1), 0 4px 5px -2px rgba(0, 0, 0, 0.12),
    0 10px 15px -5px rgba(0, 0, 0, 0.2) !important;
}
</style>
