<template lang="html">
  <div id="templates">
    <b-table responsive fixed selectable stacked="sm" head-variant="dark" hover outlined borderless :items="templates" :fields="fields" :sort-compare="mySortCompare" @row-clicked="templateDetails">
      <template v-slot:cell(titleid)="data">
        {{ data.item.title }}
      </template>
      <template v-slot:cell(update_now)="data">
        <div>
          <b-button squared block v-b-toggle="'collapse-actions'+ data.item.id" title="Actions" class="m-1" variant="dark">
            <b-icon-chevron-down />
            Actions
          </b-button>
          <b-collapse :id="'collapse-actions'+ data.item.id" accordion="template-actions">
            <b-card bg-variant="light" no-body >
              <b-button @click="updateThis(data.item.id)" squared class="m-1 text-left" title="Update Template" variant="light">
                <b-icon-arrow-repeat />
                Update
              </b-button>
              <b-button squared class="m-1 text-left" title="Remove Template" variant="light">
                <b-icon-list-ul />
                Remove
              </b-button>
            </b-card>
          </b-collapse>
        </div>
      </template>
    </b-table>
  </div>
</template>

<script>
export default {
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
    mySortCompare: function(a, b, key) {
      key = (key === 'titleid' ? 'title' : key);
      return a[key].toString().localeCompare(b[key].toString());
    },
    updateThis(id) {
      this.updateTemplate(id);
    },
    templateDetails(template) {
      this.$router.push({ path: `/templates/${template.id}` })
    }
  },
  computed: {
    templates() {
      return this.$store.state.templates.templates;
    }
  },
  mounted() {
    this.$store.dispatch("templates/loadTemplates");
  }
};
</script>

<style lang="css" scoped>
</style>