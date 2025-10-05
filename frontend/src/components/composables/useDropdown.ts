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

  const onKeydown = (event: KeyboardEvent) => {
    if (event.key === "Escape") {
      close();
    }
  };

  onMounted(() => {
    document.addEventListener("click", onClick);
    document.addEventListener("keydown", onKeydown);
  });

  onBeforeUnmount(() => {
    document.removeEventListener("click", onClick);
    document.removeEventListener("keydown", onKeydown);
  });

  return {
    isOpen,
    toggle,
    close,
  };
}
