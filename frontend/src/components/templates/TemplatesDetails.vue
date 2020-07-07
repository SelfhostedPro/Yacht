<template lang="html">
  <div v-if="template">
    <b-button type="button" @click="removeTemplate(template.id)">Delete</b-button>
    <h4>{{ template.title }}</h4>
    <p>{{ template.url }}</p>
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { mapActions } from 'vuex'

export default {
  data() {
    return {
      // templateData: null
    };
  },
  computed: {
    ...mapGetters({
      getTemplateById: 'templates/getTemplateById'
    }),
    template() {
      const templateId = this.$route.params.templateId;
      console.log("from calling function" + templateId)
      return this.getTemplateById(templateId);
    }
  },
  methods: {
    ...mapActions({
      readTemplate: "templates/readTemplate",
      readTemplates: "templates/readTemplates",
      deleteTemplate: "templates/deleteTemplate"
    }),
    removeTemplate(id) {
      // console.log(id);
      this.deleteTemplate(id);
      this.$router.push('/templates/');
    }
  },
  mounted() {
    // BUG:
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);

    // NO BUG:
    // this.readTemplates();
  },
  beforeRouterUpdates(to, from, next) {
    // BUG:
    const templateId = this.$route.params.templateId;
    this.readTemplate(templateId);

    // NO BUG:
    // this.readTemplates();
    next();
  }
};
</script>

<style lang="css" scoped>
</style>
