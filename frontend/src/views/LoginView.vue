<script setup>
import googleButtonVue from '../components/blocks/buttons/google-button.vue'
import logoVue from '../components/icons/logo.vue'

const loginWithGoogle = async () => {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/auth/google/', { credentials: 'include' });
    const data = await response.json();
    window.location.href = data.auth_url;
  } catch (error) {
    console.error('Error initiating Google login:', error);
  }
}
</script>

<template>
    <section class="login-page">
      <logoVue
        class="login-page__logo"
      />
      <h1 class="login-page__title">Log in to TimeFlow</h1>

      <googleButtonVue class="login-page__button"
        @click="loginWithGoogle"
        text="Continue with Google"
      />

      <p class="login-page__text">Don't have an account? <RouterLink to="/signup/">Sign Up</RouterLink></p>

      <p class="login-page__privacy-text">By using TimeFlow, you agree to our <a href="javascript:void();">Terms of Service</a> and <a href="javascript:void();">Privacy Policy</a>.</p>
    </section>
</template>

<style lang="scss">
@use '@/assets/scss/mixins/mixins.scss' as *;
@use '@/assets/scss/mixins/fonts.scss' as *;
@use '@/assets/scss/colors.scss' as *;
@use '@/assets/scss/mixins/functions.scss' as *;

.login-page {
  display: flex;
  align-items: center;
  flex-direction: column;

  &__logo {
    display: block;
    width: size(70px);
    height: size(70px);
    margin-bottom: size(20px);
  }

  &__title {
    font-weight: 600;
    font-size: size(50px);
    line-height: 100%;
    text-align: center;
    color: $white;
    margin-top: 0;
    margin-bottom: size(88px);
  }

  &__button {
    margin-bottom: size(44px);
  }

  &__text {
    @include bold-20;
    color: $white;
    margin-top: 0;
    margin-bottom: size(163px);

    & a {
      color: #4BB6E4;
    }
  }

  &__privacy-text {
    @include light-20;
    color: $dark-lines;
    margin: 0;

    & a {
      text-decoration: underline;
    }
  }
}
</style>
