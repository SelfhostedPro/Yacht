<template lang="html">
  <div id="templates">
    <b-table responsive :items="templatesData" :fields="fields"></b-table>
  </div>
</template>

<script>
// import axios from "axios";
export default {
  data() {
    return {
      // fields to display
      fields: [
        {
          key: 'title',
          sortable: true,
        },
        {
          key: 'url',
          sortable: true,
        },
        {
          key: 'created_at',
          sortable: true,
          formatter: "fmtDate"
        },
        {
          key: 'updated_at',
          sortable: true,
          formatter: "fmtDate"
        }
      ],
      templatesData: []
    }
  },
  methods: {
    fetchData() {
      const url = "/api/templates/";
      this.$http.get(url)
        .then(response => {
          this.templatesData = response.data.data;
        });
    },
    // format date to local string
    fmtDate(value) {
      return (new Date(Date.parse(value))).toLocaleString();
    }
  },
  mounted() {
    // load templates from api
    this.fetchData();
  }
};
</script>

<style lang="css" scoped>
</style>