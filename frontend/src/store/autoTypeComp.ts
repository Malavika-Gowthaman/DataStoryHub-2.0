import { defineStore } from "pinia";
import { ref } from "vue";

interface IAutoTypeComp {
  key: string;
  start: () => void;
}

export const useAutoTypeCompStore = defineStore("autoTypedComp", () => {
  let currentAutoTypeIndex = ref(0);
  const stackAutotypedCompoenents = ref<IAutoTypeComp[]>([]);

  const startNextAutoTypeComp = () => {
    if (
      currentAutoTypeIndex.value <= stackAutotypedCompoenents.value.length &&
      stackAutotypedCompoenents.value[currentAutoTypeIndex.value]
    ) {
      stackAutotypedCompoenents.value[currentAutoTypeIndex.value].start();
      currentAutoTypeIndex.value++;
    }
  };

  const clearAutoTypeCompStack = () => {
    currentAutoTypeIndex.value = 0;
    stackAutotypedCompoenents.value = [];
  };

  return {
    stackAutotypedCompoenents,
    clearAutoTypeCompStack,
    startNextAutoTypeComp,
  };
});
