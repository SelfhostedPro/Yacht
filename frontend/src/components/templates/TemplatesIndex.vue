<template lang="html">
  <div id="templates">
    <b-table responsive stacked="sm" head-variant="dark" hover outlined borderless :items="templatesData" :fields="fields">
      <template v-slot:cell(titleid)="data">
        <router-link :to="`/templates/${data.item.id}`">{{ data.item.title }}</router-link>
      </template>
      <template v-slot:cell(update_now)="data">
        <div>
          <b-button squared block v-b-toggle="'collapse-actions'+ data.item.id" title="Actions" class="m-1" variant="dark">
            <b-icon-chevron-down />
            Actions
          </b-button>
          <b-collapse :id="'collapse-actions'+ data.item.id" accordion="template-actions">
            <b-button @click="updateThis(data.item.id)" squared block class="m-1 text-left" title="Update Template" variant="light">
              <b-icon-arrow-repeat />
              Update
            </b-button>
            <b-button squared block class="m-1 text-left" title="Remove Template" variant="light">
              <b-icon-list-ul />
              Remove
            </b-button>
          </b-collapse>
        </div>
      </template>
    </b-table>
  </div>
</template>

<script>
import templateMixin from "@/mixins/templates";

export default {
  mixins: [templateMixin],
  data() {
    return {
      // fields to display
      fields: [
        {
          key: 'titleid',
          label: 'Title',
          sortable: true,
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
        },
        {
          key: 'update_now',
          sortable: false,
          label: '',
          headerTitle: 'Update Buttons'
        }
      ],
      templatesData: []
    }
  },
  methods: {
    /* format date to local string */
    fmtDate(value) {
      return (new Date(Date.parse(value))).toLocaleString();
    },
    updateThis(data) {
      console.log(data)
      this.updateTemplate(data);
    }
  },
  mounted() {
    this.readTemplates();
  }
};
</script>

<style lang="css" scoped>
</style>