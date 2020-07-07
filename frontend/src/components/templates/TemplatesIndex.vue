<template lang="html">
  <div id="templates">
    <b-table
      responsive
      fixed
      selectable
      stacked="sm"
      head-variant="dark"
      hover
      outlined
      borderless
      :items="templates"
      :fields="fields"
      :sort-compare="mySortCompare"
      @row-clicked="templateDetails"
    >
      <template v-slot:cell(titleid)="data">
        {{ data.item.title }}
      </template>
      <template v-slot:cell(update_now)="data">
        <div>
          <b-button
            squared
            block
            v-b-toggle="'collapse-actions' + data.item.id"
            title="Actions"
            class="m-1"
            variant="dark"
          >
            Actions
            <b-icon-chevron-down />
          </b-button>
          <b-collapse
            :id="'collapse-actions' + data.item.id"
            accordion="template-actions"
          >
            <b-card bg-variant="light" no-body>
              <b-button
                @click="updateThis(data.item.id)"
                squared
                class="d-flex px-4 align-items-center"
                title="Update Template"
                variant="light"
              >
                Update
                <b-icon-arrow-repeat class="ml-auto" />
              </b-button>
              <b-button
                v-b-modal="`delete-modal` + data.item.id"
                squared
                class="d-flex px-4 align-items-center"
                title="Remove Template"
                variant="light"
              >
                Remove
                <b-icon-dash class="ml-auto" />
              </b-button>
              <b-modal
                :id="`delete-modal` + data.item.id"
                :title="'Delete Template: ' + data.item.title"
                header-bg-variant="dark"
                header-text-variant="light"
                ok-variant="danger"
                hide-backdrop
                content-class="shadow"
              >
                <template slot="modal-footer" slot-scope="{ ok, cancel }" >
                  <div class="d-flex">
                    <b-button @click="cancel" variant="dark" > Cancel </b-button>
                    <b-button @click="removeTemplate( data.item.id );ok();" variant="danger" class=" ml-2 "> Delete </b-button>
                  </div>
                </template>
                <p>
                  Deleting this template will remove the ability to lauch all
                  apps defined by it. <br>
                  (this will have no effect on running apps)
                </p>
              </b-modal>
            </b-card>
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
          key: "titleid",
          label: "Title",
          sortable: true,
        },
        {
          key: "created_at",
          sortable: true,
          formatter: "fmtDate",
          thClass: "w-25",
        },
        {
          key: "updated_at",
          sortable: true,
          formatter: "fmtDate",
          thClass: "w-25",
        },
        {
          key: "update_now",
          sortable: false,
          label: "",
          headerTitle: "Update Buttons",
        },
      ],
      templatesData: [],
    };
  },
  methods: {
    /* format date to local string */
    fmtDate(value) {
      return new Date(Date.parse(value)).toLocaleString();
    },
    mySortCompare: function(a, b, key) {
      key = key === "titleid" ? "title" : key;
      return a[key].toString().localeCompare(b[key].toString());
    },
    updateThis(id) {
      this.updateTemplate(id);
    },
    templateDetails(template) {
      this.$router.push({ path: `/templates/${template.id}` });
    },
    removeTemplate(id) {
      console.log(id);
      this.deleteTemplate(id);
    },
  },
  computed: {
    templates() {
      return this.$store.state.templates.templates;
    },
  },
  mounted() {
    this.$store.dispatch("templates/loadTemplates");
  },
};
</script>

<style lang="css" scoped></style>
