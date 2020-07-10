<template lang="html">
  <div id="templates">
    <!-- Flexbox for button -->
      <div class="d-flex center-align-items">
      <b-form-input v-model="filter" placeholder="Type to Search" class="mr-2">
      </b-form-input>
        <!-- Plus button -->
        <b-button
          squared
          v-b-modal="'addTemplate'"
          title="Add Template"
          class="ml-auto mb-1"
          variant="dark"
        >
          <b-icon-plus />
          <!-- Add Template Modal -->
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
                  ok();
                  addTemplateSubmit();
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
      <!-- Table -->
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
        :filter="filter"
        :filter-included-fields="['title']"
        :per-page="perPage"
        :current-page="currentPage"
        @row-clicked="templateDetails"
      >
        <!-- Update column -->
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
                  @click="updateTemplate(data.item.id)"
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

      <!-- Pagination -->
      <b-pagination
        v-model="currentPage"
        :total-rows="templates.length"
        :per-page="perPage"
        aria-controls="my-table"
      ></b-pagination>

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
        @ok="deleteTemplate(selectedTemplate.id)"
      >
        <p>
          Deleting this template will remove the ability to lauch all apps
          defined by it. <br />
          (this will have no effect on running apps)
        </p>
      </b-modal>
  </div>
</template>

<script>
import { mapState } from "vuex";
// import { mapGetters } from "vuex";
import { mapActions } from "vuex";

export default {
  data() {
    return {
      filter: null,
      perPage: 5,
      currentPage: 1,
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
    templateDetails(template) {
      this.$router.push({ path: `/templates/${template.id}` });
    },
    addTemplateSubmit() {
      const data = { ...this.form };
      this.writeTemplate(data);
      this.$refs.form.reset();
    },
  },
  computed: {
    ...mapState("templates", ["templates", "loading"]),
  },
  mounted() {
    this.readTemplates();
  },
  watch: {
    templates: (oldval, newval) => {
      console.log(oldval, newval);
    },
  },
};
</script>

<style lang="css" scoped></style>
