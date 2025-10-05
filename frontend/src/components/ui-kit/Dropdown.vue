<script setup lang="ts">

</script>

<template>
<div class="dropdown">
  <slot></slot>
</div>
</template>

<style scoped lang="scss">
.dropdown {
  border-radius: 4px;
  padding: 12px;

  box-shadow: 0 0 12px 0 rgba(0, 0, 0, 0.12);
  background: var(--bg-highlight);
}
</style>
