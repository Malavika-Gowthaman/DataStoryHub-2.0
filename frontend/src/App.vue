<template>
  <Toast class="sm:max-w-2/3 lg:w-fit" />
  <MainLayout />
</template>

<script lang="ts" setup>
import MainLayout from "./layouts/MainLayout/MainLayout.vue";
import { updatePrimaryPalette } from "@primeuix/themes";
import Toast from "primevue/toast";
import { onMounted } from "vue";

onMounted(() => {
  updatePrimaryPalette({
    50: "{noir.50}",
    100: "{noir.100}",
    200: "{noir.200}",
    300: "{noir.300}",
    400: "{noir.400}",
    500: "{noir.500}",
    600: "{noir.600}",
    700: "{noir.700}",
    800: "{noir.800}",
    900: "{noir.900}",
    950: "{noir.950}",
  });
});
</script>
