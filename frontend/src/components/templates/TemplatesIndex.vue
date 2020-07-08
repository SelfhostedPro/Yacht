<template lang="html">
  <div id="templates">
    <!-- Flexbox for button -->
    <div class="d-flex center-align-items">
      <!-- Plus button -->
      <b-button
        squared
        v-b-modal="'addTemplate'"
        title="Add Template"
        class="ml-auto mb-1"
        variant="dark"
      >
        <b-icon-plus />
        <!-- Modal -->
      </b-button>
      <b-modal
        :id="'addTemplate'"
        :title="'Add Template'"
        header-bg-variant="dark"
        header-text-variant="light"
        hide-backdrop
        content-class="shadow"
      >
        <!-- Modal Footer -->
        <template slot="modal-footer" slot-scope="{ ok, cancel }">
          <div class="d-flex">
            <b-button @click="cancel" variant="dark"> Cancel </b-button>
            <b-button
              @click="
                addTemplateSubmit();
                ok();
              "
              variant="primary"
              class=" ml-2 "
            >
              Add
              <b-icon-plus />
            </b-button>
          </div>
        </template>
        <!-- Modal Content -->
        <b-form @submit.prevent="onSubmit">
          <b-form-group
            label="Title:"
            label-for="title"
            description="The title of the template."
          >
            <b-form-input
              id="title"
              v-model="form.title"
              type="text"
              placeholder="Template Name"
              required
            >
            </b-form-input>
          </b-form-group>

          <b-form-group
            label="URL:"
            label-for="url"
            description="The URL of the template."
          >
            <b-form-input
              id="title"
              v-model="form.url"
              type="url"
              placeholder="http://example.com/path/to/template.json"
              required
            >
            </b-form-input>
          </b-form-group>
        </b-form>
      </b-modal>
    </div>
    <b-table
      responsive
      fixed
      selectable
      stacked="sm"
      head-variant="dark"
      hover
      outlined
      borderless
      :items="getTemplates"
      :fields="fields"
      :sort-compare="mySortCompare"
      @row-clicked="templateDetails"
    >
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
                v-b-modal="'modal-delete'"
                squared
                class="d-flex px-4 align-items-center"
                title="Remove Template"
                variant="light"
                @click="selectedTemplate = data.item"
              >
                Delete
                <b-icon-trash class="ml-auto" />
              </b-button>
            </b-card>
          </b-collapse>
        </div>
      </template>
    </b-table>

    <!-- title="Delete Template" -->
    <b-modal
      v-if="selectedTemplate"
      id="modal-delete"
      :title="`Delete Template: &quot;${selectedTemplate.title}&quot;`"
      header-bg-variant="dark"
      header-text-variant="light"
      ok-variant="danger"
      hide-backdrop
      content-class="shadow"
      @ok="removeTemplate(selectedTemplate.id)"
    >
      <p>
        Deleting this template will remove the ability to lauch all apps defined
        by it. <br />
        (this will have no effect on running apps)
      </p>
    </b-modal>
  </div>
</template>

<script>
// import templateMixin from "@/mixins/templates";
import { mapState } from "vuex";
import { mapActions } from "vuex";
import { mapGetters } from "vuex";
export default {
  // mixins: [templateMixin],
  data() {
    return {
      // fields to display
      fields: [
        {
          key: "title",
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
      form: {},
      selectedTemplate: null,
    };
  },
  methods: {
    ...mapActions({
      readTemplates: "templates/readTemplates",
      updateTemplate: "templates/updateTemplate",
      deleteTemplate: "templates/deleteTemplate",
      writeTemplate: "templates/writeTemplate",
    }),
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
      // this.readTemplates();
    },
    templateDetails(template) {
      this.$router.push({ path: `/templates/${template.id}` });
    },
    removeTemplate(id) {
      console.log(id);
      this.deleteTemplate(id);
      this.readTemplates();
    },
    addTemplateSubmit() {
      const data = { ...this.form };
      this.writeTemplate(data);
    },
  },
  computed: {
    ...mapState("templates", ["templates"]),
    ...mapGetters({
      getTemplates: "templates/getTemplates",
    }),
  },
  mounted() {
    this.readTemplates();
  },
};
</script>

<style lang="css" scoped></style>
