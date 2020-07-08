<template lang="html">
  <div v-if="currentTemplate">
    <h2>{{ currentTemplate.title }}</h2>
    <p>{{ currentTemplate.url }}</p>
    <b-button type="button" @click="removeTemplate(currentTemplate.id)">Delete</b-button>    
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { mapActions } from 'vuex'
import { mapState } from 'vuex'
export default {
  data() {
    return {
    };
  },
  computed: {
    ...mapState("templates", [
      "currentTemplate"
    ]),
    ...mapGetters({
      getTemplateById: "templates/getTemplateById"
    }),
    // currently unused, see currentTemplate
    template() {
      const templateId = this.$route.params.templateId;
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