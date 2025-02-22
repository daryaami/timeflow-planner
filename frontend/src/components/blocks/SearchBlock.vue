<template>
  <div class="search">
    <button class="search__button">

    </button>
  </div>
</template>

<script>
export default {

}
</script>

<style lang="scss">
@use '@/assets/scss/mixins/resets.scss' as *;

.search {
  &__button {
    @include reset-button;
    // @include search-icon;
    width: 24px;
    height: 24px;
    display: block;
    background-size: 100%;
  }
}
</style>
