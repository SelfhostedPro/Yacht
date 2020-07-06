<template lang="html">
  <div id="templates">
    <b-table responsive :items="templatesData" :fields="fields">
      <template v-slot:cell(titleid)="data">
        <router-link :to="`/templates/${data.item.id}`">{{ data.item.title }}</router-link>
      </template>
    </b-table>
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
          key: 'titleid',
          label: 'Title',
          sortable: true,
          tdClass: "text-left"
        },
        {
          key: 'created_at',
          sortable: true,
          formatter: "fmtDate",
          thClass: "w-25"
        },
        {
          key: 'updated_at',
          sortable: true,
          formatter: "fmtDate",
          thClass: "w-25"
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
