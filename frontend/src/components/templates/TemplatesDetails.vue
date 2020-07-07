<template lang="html">
  <div v-if="templateData">
    <b-button type="button" @click="removeTemplate">Delete</b-button>
    <h4>{{ templateData.title }}</h4>
    <p>{{ templateData.url }}</p>
  </div>
</template>

<script>
import templateMixin from "@/mixins/templates";

export default {
  mixins: [templateMixin],
  data() {
    return {
      // templateData: null
    };
  },
  methods: {
    removeTemplate() {
      console.log(this.templateData.id);
      this.deleteTemplate(this.templateData.id);
    }
  },
  mounted() {
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);
  },
  beforeRouterUpdates(to, from, next) {
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);
    next();
  }
};
</script>

<style lang="css" scoped>
</style>
