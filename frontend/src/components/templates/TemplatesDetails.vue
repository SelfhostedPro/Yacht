<template lang="html">
  <div v-if="templateData">
    <h4>{{ templateData.title }}</h4>
    <p>{{ templateData.url }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      templateData: null
    };
  },
  methods: {
    fetchTemplateData() { // possible init => _fetchTemplateData(templateId)
      const templateId = this.$route.params.templateId;
      const url = `/api/templates/${templateId}`;
      this.$http.get(url)
        .then(response => {
          this.templateData = response.data.data;
        })
        .catch(error => {
          console.error(error);
          this.$router.push('/dashboard');
        });
    }
  },
  mounted() {
    this.fetchTemplateData();
  },
  beforeRouterUpdates(to, from, next) {
    this.fetchTemplateData();
    next();
  }
};
</script>

<style lang="css" scoped>
</style>