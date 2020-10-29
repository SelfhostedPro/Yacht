<template>
  <div class="page">
    <v-card color="foreground">
      <v-fade-transition>
        <v-progress-linear
          indeterminate
          v-if="isLoading"
          color="primary"
          bottom
        />
      </v-fade-transition>
      <v-card-title>
        {{ project.name }}
      </v-card-title>
      <v-card-subtitle>
        <v-chip
          outlined
          small
          color="orange lighten-1"
          class="align-center mt-1"
          label
          v-if="project.inUse == false"
          >Unused</v-chip
        >
      </v-card-subtitle>
    </v-card>
    <v-card color="foreground" class="mt-2">
      <v-card-title>
        Project Details
      </v-card-title>
      <v-list color="foreground" dense>
        <v-list-item>
          <v-list-item-content>
            Name
          </v-list-item-content>
          <v-list-item-content>
            {{ project.name }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Path
          </v-list-item-content>
          <v-list-item-content>
            {{ project.path }}
          </v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>
            Version
          </v-list-item-content>
          <v-list-item-content>
            {{ project.version }}
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card>
    <v-card color="foreground" class="mt-2">
      <v-card-title>
        Services
      </v-card-title>
      <v-card-text>
        <v-expansion-panels>
          <v-expansion-panel
            v-for="(service, index) in Object.keys(project.services)"
            :key="index"
          >
            <v-expansion-panel-header color="secondary">
              <v-row no-gutters style="max-height: 20px;">
                <v-col cols="2">{{ service }} </v-col>
                <v-col cols="5" class="text--secondary">
                  ({{ project.services[service].image || "No Image" }})
                </v-col>
                <v-col cols="2" class="text--secondary">
                  {{
                    getStatus(
                      project.services[service].container_name || service
                    ) || "missing"
                  }}
                </v-col>
              </v-row>
            </v-expansion-panel-header>
            <v-expansion-panel-content color="foreground">
              <div class="text-center mt-2">
                <v-item-group dense class="v-btn-toggle">
                  <v-btn
                    small
                    @click="
                      projectAppAction({
                        Project: project.name,
                        Name: service,
                        Action: 'start',
                      })
                    "
                  >
                    <v-icon small>mdi-play</v-icon>
                    start
                  </v-btn>
                  <v-btn
                    small
                    @click="
                      projectAppAction({
                        Project: project.name,
                        Name: service,
                        Action: 'stop',
                      })
                    "
                  >
                    <v-icon small>mdi-stop</v-icon>
                    stop
                  </v-btn>
                  <v-btn
                    small
                    @click="
                      projectAppAction({
                        Project: project.name,
                        Name: service,
                        Action: 'restart',
                      })
                    "
                  >
                    <v-icon small>mdi-refresh</v-icon>
                    restart
                  </v-btn>
                  <v-divider vertical />
                  <v-btn
                    small
                    @click="
                      projectAppAction({
                        Project: project.name,
                        Name: service,
                        Action: 'pull',
                      })
                    "
                  >
                    <v-icon small>mdi-update</v-icon>
                    pull
                  </v-btn>
                  <v-divider vertical />
                  <v-btn
                    small
                    @click="
                      projectAppAction({
                        Project: project.name,
                        Name: service,
                        Action: 'kill',
                      })
                    "
                  >
                    <v-icon small>mdi-fire</v-icon>
                    kill
                  </v-btn>
                  <v-btn
                    small
                    @click="
                      projectAppAction({
                        Project: project.name,
                        Name: service,
                        Action: 'rm',
                      })
                    "
                  >
                    <v-icon small>mdi-delete</v-icon>
                    remove
                  </v-btn>
                </v-item-group>
              </div>
              <v-list color="foreground" dense>
                <v-list-item v-if="project.services[service].container_name">
                  <v-list-item-content>
                    Container Name
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].container_name }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].image">
                  <v-list-item-content>
                    Image
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].image }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].env_file">
                  <v-list-item-content>
                    Env File
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].env_file.join(", ") }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].depends_on">
                  <v-list-item-content>
                    Depends on
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].depends_on.join(", ") }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].restart">
                  <v-list-item-content>
                    Restart Policy
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].restart }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].read_only">
                  <v-list-item-content>
                    Read Only
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].read_only }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].networks">
                  <v-list-item-content>
                    Networks
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].networks.join(", ") }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].ports">
                  <v-list-item-content>
                    Ports
                  </v-list-item-content>
                  <v-list-item-content>
                    {{ project.services[service].ports.join(", ") }}
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].volumes">
                  <v-list-item-content>
                    Volumes
                  </v-list-item-content>
                  <v-list-item-content>
                    <v-card outlined tile>
                      <v-simple-table class="secondary" dense>
                        <thead>
                          <tr>
                            <th>
                              Host
                            </th>
                            <th>
                              Container
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="(value, index) in project.services[service]
                              .volumes"
                            :key="index"
                          >
                            <td>
                              {{ value.split(":")[0] }}
                            </td>
                            <td>
                              {{ value.split(":")[1] }}
                            </td>
                          </tr>
                        </tbody>
                      </v-simple-table>
                    </v-card>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].environment">
                  <v-list-item-content>
                    Environment
                  </v-list-item-content>
                  <v-list-item-content>
                    <v-card outlined tile>
                      <v-simple-table class="secondary" dense>
                        <thead>
                          <tr>
                            <th>
                              Variable
                            </th>
                            <th>
                              Value
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="(value, index) in project.services[service]
                              .environment"
                            :key="index"
                          >
                            <td>
                              {{ value.split("=")[0] }}
                            </td>
                            <td>
                              {{ value.split("=")[1] }}
                            </td>
                          </tr>
                        </tbody>
                      </v-simple-table>
                    </v-card>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].labels">
                  <v-list-item-content>
                    Labels
                  </v-list-item-content>
                  <v-list-item-content>
                    <v-card outlined tile>
                      <v-simple-table class="secondary" dense>
                        <thead>
                          <tr>
                            <th>
                              Label
                            </th>
                            <th>
                              Value
                            </th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr
                            v-for="(value, index) in project.services[service]
                              .labels"
                            :key="index"
                          >
                            <td>
                              {{ value.split("=")[0] }}
                            </td>
                            <td>
                              {{ value.split("=")[1] }}
                            </td>
                          </tr>
                        </tbody>
                      </v-simple-table>
                    </v-card>
                  </v-list-item-content>
                </v-list-item>
                <v-list-item v-if="project.services[service].command">
                  <v-list-item-content>
                    Command
                  </v-list-item-content>
                  <v-list-item-content>
                    <v-card outlined tile>
                      <v-simple-table class="secondary" dense>
                        <tbody>
                          <tr
                            v-for="(value, index) in project.services[service]
                              .command"
                            :key="index"
                          >
                            <td>
                              {{ value }}
                            </td>
                          </tr>
                        </tbody>
                      </v-simple-table>
                    </v-card>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-expansion-panel-content>
          </v-expansion-panel>
        </v-expansion-panels>
      </v-card-text>
    </v-card>
    <v-card color="foreground" v-if="project.networks" class="mt-2">
      <v-card-title>
        Networks
      </v-card-title>
      <v-card-text>
        {{ project.networks.join(", ") }}
      </v-card-text>
    </v-card>
    <v-card color="foreground" v-if="project.volumes" class="mt-2">
      <v-card-title>
        Volumes
      </v-card-title>
      <v-card-text>
        {{ project.volumes.join(", ") }}
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters, mapState } from "vuex";

export default {
  data() {
    return {};
  },
  computed: {
    ...mapState("projects", ["project", "projects", "isLoading"]),
    ...mapState("apps", ["apps"]),
    ...mapGetters({
      getProjectByName: "projects/getProjectByName",
    }),
    project() {
      const projectName = this.$route.params.projectName;
      return this.getProjectByName(projectName);
    },
  },
  methods: {
    ...mapActions({
      readProject: "projects/readProject",
      projectAppAction: "projects/ProjectAppAction",
      readApps: "apps/readApps",
    }),
    getStatus(name) {
      for (var app in this.apps) {
        console.log(
          this.project.name + "_" + name + "_1" + " vs " + this.apps[app].name
        );
        if (
          this.apps[app].name == name ||
          this.apps[app].name == this.project.name + "_" + name + "_1"
        ) {
          return this.apps[app].State.Status;
        }
      }
    },

    reload() {
      const projectName = this.$route.params.projectName;
      this.readProject(projectName);
      this.readApps();
    },
  },
  created() {
    const projectName = this.$route.params.projectName;
    this.readProject(projectName);
    this.readApps();
  },
};
</script>

<style scoped></style>
