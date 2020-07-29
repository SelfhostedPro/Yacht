<template>
  <ValidationObserver ref="obs1" v-slot="{ invalid }">
    <v-card class="elevation-12 pb-8">
      <v-toolbar color="primary" dark flat>
        <v-toolbar-title>Change Password</v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        You can also change just your username here (or both your username and
        password).
        <v-form @keyup.native.enter="onSubmit()">
          <ValidationProvider
            name="username"
            rules="required"
            immediate
            v-slot="{ errors, valid }"
          >
            <v-text-field
              label="Username"
              v-model="username"
              :error-messages="errors"
              :success="valid"
              required
            />
          </ValidationProvider>

          <ValidationProvider
            name="oldPassword"
            rules="required"
            v-slot="{ errors, valid }"
          >
            <v-text-field
              label="Old Password"
              v-model="oldPassword"
              :error-messages="errors"
              :success="valid"
              :type="show1 ? 'text' : 'password'"
              :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
              required
              @click:append="show1 = !show1"
            />
          </ValidationProvider>
          <ValidationProvider
            name="newPassword"
            rules=""
            v-slot="{ errors, valid }"
          >
            <v-text-field
              label="New Password"
              v-model="newPassword"
              :error-messages="errors"
              :success="valid"
              :type="show2 ? 'text' : 'password'"
              :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="show2 = !show2"
            />
          </ValidationProvider>
          <ValidationProvider
            name="confirm"
            rules="confirmed:newPassword"
            v-slot="{ errors, valid }"
          >
            <v-text-field
              label="Confirm New Password"
              v-model="confirm"
              :error-messages="errors"
              :success="valid"
              :type="show3 ? 'text' : 'password'"
              :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
              @click:append="show3 = !show3"
            />
          </ValidationProvider>
          <v-btn
            class="float-right"
            @click="onSubmit()"
            color="primary"
            :disabled="invalid"
            >Change User Info</v-btn
          >
        </v-form>
      </v-card-text>
    </v-card>
  </ValidationObserver>
</template>

<script>
import { ValidationObserver, ValidationProvider } from "vee-validate";
import { mapActions } from "vuex";
export default {
  components: {
    ValidationProvider,
    ValidationObserver,
  },
  props: ["currentUsername"],
  data() {
    return {
      username: this.currentUsername || "",
      oldPassword: "",
      newPassword: "",
      confirm: "",
      show1: false,
      show2: false,
      show3: false,
    };
  },
  methods: {
    ...mapActions({
      login: "auth/AUTH_CHANGE_PASS",
    }),
    onSubmit() {
      this.login({
        username: this.username,
        newPassword: this.newPassword,
        oldPassword: this.oldPassword,
      }
    );
    },
  }
};
</script>

<style lang="css" scope>
</style>
