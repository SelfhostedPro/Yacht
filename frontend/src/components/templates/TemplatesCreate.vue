<template lang="html">
  <div>
    <b-card style="max-width: 75%;" header="Add a Template" header-class="h2" header-text-variant="white" header-bg-variant="dark" border-variant="dark" class="mx-auto mt-5">
      <b-form @submit.prevent="onSubmit">
          <b-form-group
            label="Title:"
            label-for="title"
            description="The title of the template.">
            <b-form-input
              id="title"
              v-model="form.title"
              type="text"
              placeholder="Template Name"
              required
              >
            </b-form-input>
          </b-form-group>

          <b-form-group
            label="URL:"
            label-for="url"
            description="The URL of the template.">
            <b-form-input
              id="title"
              v-model="form.url"
              type="url"
              placeholder="http://example.com/path/to/template.json"
              required
              >
            </b-form-input>
          </b-form-group>
          <b-button type="submit" class="mr-3" variant="primary">Submit</b-button>
          <b-button type="reset" class="ml-3" variant="danger">Reset</b-button>
      </b-form>
    </b-card>
  </div>
</template>

<script>
// import templateMixin from "@/mixins/templates";
import { mapActions } from "vuex";

export default {
  // mixins: [templateMixin],
  data() {
    return {
      form: {
      }
    };
  },
  methods: {
    ...mapActions({
      writeTemplate: "templates/writeTemplate",
    }),
    onSubmit() {
      const data = { ...this.form };
      this.writeTemplate(data);
      // this.form = {
      //   title: "Untitled Template 2",
      //   url: "http://localhost:8000/static/template.json"
      // };
      // this.refs.form.reset();
      this.$router.push('/templates')
    },
    onReset() {
      // not really necessary
    }
  },
  mounted() {
  },
  // beforeRouterUpdates(to, from, next) {}

};
</script>

<style lang="css" scoped>
</style>
