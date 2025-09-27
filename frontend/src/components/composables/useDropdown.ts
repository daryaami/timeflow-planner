// composables/useDropdown.ts
import { ref, onMounted, onBeforeUnmount, Ref } from "vue";

export function useDropdown(rootEl: Ref<HTMLElement | null>) {
  const isOpen = ref(false);

  const toggle = () => {
    isOpen.value = !isOpen.value;
  };

  const close = () => {
    isOpen.value = false;
  };

  const onClick = (event: MouseEvent) => {
    const target = event.target as Node;
    if (rootEl.value && !rootEl.value.contains(target)) {
      close();
    }
  };

  onMounted(() => {
    document.addEventListener("click", onClick);
  });

  onBeforeUnmount(() => {
    document.removeEventListener("click", onClick);
  });

  return {
    isOpen,
    toggle,
    close,
  };
}
