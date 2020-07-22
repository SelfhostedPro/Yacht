<template lang="html">
  <div class="template-form component">
    <v-card>
      <v-card-title>
        New Template
      </v-card-title>
      <v-card-text>
        <v-form ref="form" @submit.prevent="submit">
          <v-text-field
            label="Title"
            v-model="form.title"
            :rules="titleRules"
            required
          ></v-text-field>
          <v-text-field
            label="URL"
            v-model="form.url"
            :rules="urlRules"
            required
          ></v-text-field>
          <v-btn class="mr-4" type="submit" @click="submit">Submit</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
  data: () => ({
    form: {
      title: "",
      url: "",
    },
    titleRules: [
      (value) => !!value || "Required.",
      (value) => {
        const valid =
          (value.trim() || "").length > 1 && (value.trim() || "").length < 256;
        return valid || "Length between 2 and 255 Characters.";
      },
    ],
    urlRules: [
      (value) => !!value || "Required.",
      (value) => {
        const pattern = /https?:\/\/(([a-z0-9$-_@.&+!*"'(),]+(\.[a-z0-9$-_ @.&+!*"'(),]+)*)|(\d+.\d+.\d+.\d+))(:\d+)?\/.*/i;
        return pattern.test(value) || "Invalid URL";
      },
    ],
  }),
  methods: {
    ...mapActions({
      writeTemplate: "templates/writeTemplate",
    }),
    submit() {
      const data = { ...this.form };
      console.log("submit", data);
      this.writeTemplate(data);
      this.$router.push("/templates/");
    },
  },
};
</script>

<style lang="css" scoped></style>
