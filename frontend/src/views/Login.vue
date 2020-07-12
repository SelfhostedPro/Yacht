<template lang="html">
  <div class="home text-center">
    <login-form />
  </div>
</template>

<script>
import LoginForm from "@/components/auth/LoginForm.vue";

export default {
  components: {
    LoginForm
  }
};
</script>

<style lang="scss" scoped>
  @import "@/assets/_custom.scss";
  @import "~bootstrap/scss/bootstrap.scss";
  @import '~bootstrap-vue/dist/bootstrap-vue.css';
</style>
