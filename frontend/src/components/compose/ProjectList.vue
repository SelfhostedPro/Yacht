<template lang="html">
  <div class="projects-list component" style="max-width: 90%">
    <v-card color='foreground'>
      <v-fade-transition>
        <v-progress-linear
          indeterminate
          v-if="isLoading"
          color="primary"
          bottom
        />
      </v-fade-transition>
      <v-card-title>
        Projects
        <v-spacer />
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          label="Search"
          single-line
          hide-details
        ></v-text-field>
      </v-card-title>

      <v-data-table
        style="max-width: 99%;"
        class="mx-auto project-datatable foreground"
        :headers="headers"
        :items="projects"
        :items-per-page="10"
        :search="search"
        @click:row="handleRowClick"
      >
        <template slot="no-data">
          <div>
            No Projects available.
          </div>
        </template>
        <template v-slot:item.Name="{ item }">
          <div class="d-flex">
            <span class="align-streatch text-truncate nametext mt-2">{{
              item.name
            }}</span>
            <v-spacer />

            <v-chip
              outlined
              small
              color="orange lighten-1"
              class="align-center mt-1"
              label
              v-if="item.inUse == false"
              >Unused</v-chip
            >
            <v-menu close-on-click close-on-content-click offset-y>
              <template v-slot:activator="{ on, attrs }">
                <v-btn
                  icon
                  class="align-streatch"
                  size="small"
                  v-bind="attrs"
                  v-on="on"
                >
                  <v-icon>mdi-dots-horizontal</v-icon>
                </v-btn>
              </template>
              <v-list color='foreground' dense>
                <v-list-item @click="projectDetails(item.Name)">
                  <v-list-item-icon>
                    <v-icon>mdi-eye</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>View</v-list-item-title>
                </v-list-item>
                <v-divider />
                <v-list-item
                  @click="
                    selectedProject = item;
                    deleteDialog = true;
                  "
                >
                  <v-list-item-icon>
                    <v-icon>mdi-delete</v-icon>
                  </v-list-item-icon>
                  <v-list-item-title>Delete</v-list-item-title>
                </v-list-item>
              </v-list>
            </v-menu>
          </div>
        </template>
        <template v-slot:item.Version="{ item }">
          <div class="projectcell">
            <span
              class="d-inline-block text-truncate idtext"
            >
              {{ item.version }}
            </span>
          </div>
        </template>
        <template v-slot:item.Path="{ item }" class="idcell">
          <div class="idcell">
            <span class="d-inline-block text-truncate idtext">
              {{ item.path }}
            </span>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <v-dialog v-if="selectedProject" v-model="deleteDialog" max-width="290">
      <v-card>
        <v-card-title class="headline" style="word-break: break-all;">
          Delete the project?
        </v-card-title>
        <v-card-text>
          Are you sure you want to permanently delete the project?<br />
          This action cannot be revoked.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="deleteDialog = false">
            Cancel
          </v-btn>
          <v-btn
            text
            color="error"
            @click="
              deleteProject(selectedProject.Name);
              deleteDialog = false;
            "
          >
            Delete
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { mapActions, mapState } from "vuex";
export default {
  data() {
    return {
      selectedProject: null,
      deleteDialog: false,
      form: {
        name: ""
      },
      createDialog: false,
      search: "",
      headers: [
        {
          text: "Name",
          value: "Name",
          sortable: true
        },
        {
          text: "Version",
          value: "Version",
          sortable: true
        },
        {
          text: "Path",
          value: "Path",
          sortable: true
        }
      ]
    };
  },
  methods: {
    ...mapActions({
      readProjects: "projects/readProjects",
      writeProjects: "projects/writeProject"
    }),
    handleRowClick(item) {
      this.$router.push({ path: `/projects/${item.name}` });
    },
    projectDetails(projectname) {
      this.$router.push({ path: `/projects/${projectname}` });
    },
  },
  computed: {
    ...mapState("projects", ["projects", "isLoading"])
  },
  mounted() {
    this.readProjects();
  }
};
</script>

<style lang="css" scoped>
</style>
