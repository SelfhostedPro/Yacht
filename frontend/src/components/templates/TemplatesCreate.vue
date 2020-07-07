<template lang="html">
  <div>
    <b-form @submit.prevent="onSubmit">
      <b-form-group
        label="Title:"
        label-for="title"
        description="The title of the template.">
        <b-form-input
          id="title"
          v-model="form.title"
          type="text"
          placeholder="Untitled Template"
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
          placeholder="http://localhost/path/to/template.json"
          required
          >
        </b-form-input>
      </b-form-group>

      <b-button type="submit" variant="primary">Submit</b-button>
      <b-button type="reset" variant="danger">Reset</b-button>
    </b-form>
  </div>
</template>

<script>
import templateMixin from "@/mixins/templates";

export default {
  mixins: [templateMixin],
  data() {
    return {
      form: {
        title: "Untitled Template 1",
        url: "http://localhost:5000/static/template.json"
      }
    };
  },
  methods: {
    onSubmit() {
      const data = { ...this.form };
      this.writeTemplate(data);
      // this.form = {
      //   title: "Untitled Template 2",
      //   url: "http://localhost:8000/static/template.json"
      // };
      // this.refs.form.reset();
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
