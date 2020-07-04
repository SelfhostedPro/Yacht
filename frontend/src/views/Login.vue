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

<style lang="css" scoped></style>
