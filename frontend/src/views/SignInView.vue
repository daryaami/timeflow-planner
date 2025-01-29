<template>
  <div>
    <!-- Кнопка Google Sign-In -->
    <div id="google-signin-button"></div>
  </div>
</template>

<script>
export default {
  mounted() {
    // Инициализация Google Sign-In при монтировании компонента
    window.gapi.load('auth2', () => {
      const auth2 = window.gapi.auth2.init({
        client_id: 'YOUR_GOOGLE_CLIENT_ID.apps.googleusercontent.com', // Ваш client_id
      });

      // Создание кнопки Google Sign-In
      auth2.attachClickHandler(
        document.getElementById('google-signin-button'),
        {},
        this.onSignIn,
        this.onFailure
      );
    });
  },

  methods: {
    // Обработчик успешного входа
    onSignIn(googleUser) {
      // Получаем ID токен
      const id_token = googleUser.getAuthResponse().id_token;

      console.log('ID токен:', id_token);

      // Отправляем ID токен на сервер
      // fetch('/api/auth/google/token/', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({ id_token: id_token }),
      // })
      //   .then((response) => response.json())
      //   .then((data) => {
      //     console.log('Logged in successfully:', data);
      //     // Можно сохранить JWT в localStorage или vuex, если нужно
      //   })
      //   .catch((error) => {
      //     console.error('Error:', error);
      //   });
    },

    // Обработчик ошибок
    onFailure(error) {
      console.error('Google Sign-In Error:', error);
    },
  },
};
</script>

<style scoped>
/* Стили для кнопки Google Sign-In (если нужно) */
</style>
