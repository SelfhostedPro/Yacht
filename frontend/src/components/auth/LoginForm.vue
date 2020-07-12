<template lang="html">
  <b-form
    ref="form"
    @submit.prevent="onSubmit"
    class="form-signin mt-5 text-center"
  >
    <!-- add validation for required to both fields -->
    <img
      class="mb-4"
      alt="Vue logo"
      src="../../assets/logo.png"
      width="72"
      height="72"
    />
    <h1 class="h3 mb-3 font-weight-normal">Please sign in</h1>
    <label for="username" class="sr-only">Username</label>
    <b-input
      id="username"
      class="form-control"
      v-model="username"
      type="text"
      placeholder="Username"
      autofocus
    />
    <label for="password" class="sr-only">Password</label>
    <b-input
      id="password"
      class="form-control"
      v-model="password"
      type="password"
      placeholder="Password"
    />
    <b-button type="submit" variant="primary" size="lg" block>Sign in</b-button>
  </b-form>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  methods: {
    ...mapActions({
      login: "auth/login"
    }),
    onSubmit() {
      this.login({
        username: this.username,
        password: this.password
      });
      this.password = "";
      // this.$refs.form.reset();
    }
  }
};
</script>

<style lang="css" scope>
.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="text"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
