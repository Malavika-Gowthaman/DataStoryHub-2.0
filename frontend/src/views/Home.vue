<template>
  <!-- Main Content -->
  <div class="w-full flex flex-col p-4">
    <!-- Page Title -->
    <AutoTyped
      value="Seamless Conversational AI"
      v-slot="slotProps"
      start-next-once-done
      :speed="20"
    >
      <h1
        class="text-lg sm:text-xl md:text-3xl font-bold text-center text-purple-300"
      >
        {{ slotProps.typedValue }}
      </h1>
    </AutoTyped>

    <div class="flex flex-col md:gap-4 mt-6 sm:px-4 md:px-20 md:py-5">
      <AutoTyped
        :value="'Hello, Khushi!'"
        v-slot="slotProps"
        @done:typed="autoTypeCompStore.startNextAutoTypeComp()"
        :speed="50"
      >
        <h1
          class="text-xl sm:text-2xl font-bold text-purple-200 text-center sm:text-left"
        >
          {{ slotProps.typedValue }}
        </h1>
      </AutoTyped>

      <AutoTyped
        :speed="50"
        value="How may I assist you today?"
        v-slot="slotProps"
        @done:typed="autoTypeCompStore.startNextAutoTypeComp()"
      >
        <span class="text-md sm:text-lg text-center sm:text-left"
          >{{ slotProps.typedValue }}
        </span>
      </AutoTyped>

      <!-- Cards Section -->
      <div
        class="grid grid-cols-1 sm:grid-cols-2 gap-4 md:gap-6 max-w-4xl mx-auto mt-4"
      >
        <Card
          class="border border-gray-600"
          v-for="(data, ind) in cardData"
          :key="ind"
        >
          <template #title>{{ data.title }}</template>
          <template #content>
            {{ data.description }}
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import Card from "../components/base/BaseCard.vue";
import AutoTyped from "../components/AutoTyped.vue";
import { useAutoTypeCompStore } from "../store/autoTypeComp";

const cardData = [
  {
    title: "The Impact of Technology on Communication",
    description:
      "In today's digital age, communication methods have evolved significantly. Some argue that technology has improved communication.",
  },
  {
    title: "The Role of Education in Shaping Society",
    description:
      "Education plays a crucial role in shaping individuals and societies. Some advocate for free education, while others emphasize the importance of personal responsibility.",
  },
  {
    title: "The Environmental Consequences of Urbanization",
    description:
      " As cities expand, environmental challenges arise. Urbanization affects ecosystems, air quality, and community well-being.",
  },
  {
    title: "The Value of Handwriting in the Digital Era",
    description:
      "With the decline of handwritten communication, the art of writing by hand faces challenges. Investigate the reasons behind this shift and evaluate whether it is positive or negative for individuals and society.",
  },
];

onMounted(() => {
  autoTypeCompStore.startNextAutoTypeComp();
});

const autoTypeCompStore = useAutoTypeCompStore();
</script>
