<template lang="html">
  <div class="apps-form component">
    <h1>
      Deploy {{ form.title }}
      <v-btn
        v-if="!this.$route.params.appId"
        tile
        :to="{ name: 'View Templates' }"
        class="primary float-right"
      >
        <v-icon>mdi-plus</v-icon> From Template
      </v-btn>
    </h1>
    <v-stepper v-model="deployStep">
      <v-fade-transition>
        <v-progress-linear
          indeterminate
          v-if="isLoading"
          color="primary"
          bottom
        />
      </v-fade-transition>
      <v-stepper-header>
        <v-stepper-step step="1" :complete="deployStep > 1">
          Basics
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="2" :complete="deployStep > 2">
          Ports
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="3" :complete="deployStep > 3">
          Volumes
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="4" :complete="deployStep > 4">
          Environment
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <ValidationObserver ref="obs1" v-slot="{ invalid }">
            <form>
              <ValidationProvider
                name="Name"
                rules="required"
                v-slot="{ errors, valid }"
              >
                <v-text-field
                  label="Name"
                  placeholder="My Container"
                  v-model="form.name"
                  :error-messages="errors"
                  :success="valid"
                  required
                ></v-text-field>
              </ValidationProvider>
              <ValidationProvider
                name="Image"
                rules="required"
                v-slot="{ errors, valid }"
              >
                <v-text-field
                  label="Image"
                  placeholder="image:my-image"
                  v-model="form.image"
                  :error-messages="errors"
                  :success="valid"
                  required
                ></v-text-field>
              </ValidationProvider>
              <ValidationProvider
                name="Restart Policy"
                rules="required"
                v-slot="{ errors, valid }"
              >
                <v-select
                  :items="['always', 'on-failure', 'unless-stopped']"
                  label="Restart Policy"
                  v-model="form['restart_policy']"
                  :error-messages="errors"
                  :success="valid"
                  required
                ></v-select>
              </ValidationProvider>
            </form>
            <v-btn color="primary" @click="deployStep += 1" :disabled="invalid">
              Continue
            </v-btn>
          </ValidationObserver>
        </v-stepper-content>

        <v-stepper-content step="2">
          <ValidationObserver ref="obs2" v-slot="{ invalid }">
            <form>
              <transition-group
                name="slide"
                enter-active-class="animated fadeInLeft fast-anim"
                leave-active-class="animated fadeOutLeft fast-anim"
              >
                <v-row v-for="(item, index) in form.ports" :key="index">
                  <v-col>
                    <ValidationProvider
                      name="Container"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        type="number"
                        label="Container"
                        placeholder="80"
                        min="0"
                        max="65535"
                        v-model="item['cport']"
                        :error-messages="errors"
                        :success="valid"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col>
                    <ValidationProvider
                      name="Host"
                      rules=""
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        type="number"
                        label="Host"
                        placeholder="80"
                        min="0"
                        max="65535"
                        v-model="item['hport']"
                        :error-messages="errors"
                        :success="valid"
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col>
                    <ValidationProvider
                      name="Protocol"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-select
                        :items="['tcp', 'udp']"
                        label="Protocol"
                        v-model="item['proto']"
                        :error-messages="errors"
                        :success="valid"
                        required
                      ></v-select>
                    </ValidationProvider>
                  </v-col>

                  <v-col class="d-flex justify-end" cols="1">
                    <v-btn
                      icon
                      class="align-self-center"
                      @click="removePort(index)"
                    >
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </transition-group>
              <v-row>
                <v-col cols="12" class="d-flex justify-end">
                  <v-btn icon class="align-self-center" @click="addPort">
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </form>
            <v-btn color="secondary" @click="deployStep -= 1" class="mx-2">
              Back
            </v-btn>
            <v-btn color="primary" @click="deployStep += 1" :disabled="invalid">
              Continue
            </v-btn>
          </ValidationObserver>
        </v-stepper-content>

        <v-stepper-content step="3">
          <ValidationObserver ref="obs3" v-slot="{ invalid }">
            <form>
              <transition-group
                name="slide"
                enter-active-class="animated fadeInLeft fast-anim"
                leave-active-class="animated fadeOutLeft fast-anim"
              >
                <v-row v-for="(item, index) in form.volumes" :key="index">
                  <v-col>
                    <ValidationProvider
                      name="Container"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        label="Container"
                        placeholder="/share"
                        v-model="item['container']"
                        :error-messages="errors"
                        :success="valid"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col>
                    <ValidationProvider
                      name="Host"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        label="Host"
                        placeholder="/yacht/image/share"
                        v-model="item['bind']"
                        :error-messages="errors"
                        :success="valid"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col class="d-flex justify-end" cols="1">
                    <v-btn
                      icon
                      class="align-self-center"
                      @click="removeVolume(index)"
                    >
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </transition-group>
              <v-row>
                <v-col cols="12" class="d-flex justify-end">
                  <v-btn icon class="align-self-center" @click="addVolume">
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </form>
            <v-btn color="secondary" @click="deployStep -= 1" class="mx-2">
              Back
            </v-btn>
            <v-btn color="primary" @click="deployStep += 1" :disabled="invalid">
              Continue
            </v-btn>
          </ValidationObserver>
        </v-stepper-content>

        <v-stepper-content step="4">
          <ValidationObserver ref="obs4" v-slot="{ invalid }">
            <form>
              <transition-group
                name="slide"
                enter-active-class="animated fadeInLeft fast-anim"
                leave-active-class="animated fadeOutLeft fast-anim"
              >
                <v-row v-for="(item, index) in form.env" :key="index">
                  <v-col>
                    <ValidationProvider
                      name="Name"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        label="Name"
                        v-model="item['name']"
                        :error-messages="errors"
                        :success="valid"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col>
                    <ValidationProvider
                      name="Value"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        label="Value"
                        v-model="item['default']"
                        :error-messages="errors"
                        :success="valid"
                        :messages="item.description"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col class="d-flex justify-end" cols="1">
                    <v-btn
                      icon
                      class="align-self-center"
                      @click="removeEnv(index)"
                    >
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </transition-group>
              <v-row>
                <v-col cols="12" class="d-flex justify-end">
                  <v-btn icon class="align-self-center" @click="addEnv">
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </form>
            <v-btn color="secondary" @click="deployStep -= 1" class="mx-2">
              Back
            </v-btn>
            <v-btn color="primary" @click="nextStep(4)" :disabled="invalid">
              <div v-if="isLoading">
                Deploying
                <v-progress-circular
                  indeterminate
                  color="white"
                  size="15"
                  width="2"
                />
              </div>
              <div v-else>Deploy</div>
            </v-btn>
          </ValidationObserver>
        </v-stepper-content>
      </v-stepper-items>
    </v-stepper>
    <v-card color="secondary" class="mt-5">
      <v-card-title>
        Advanced
      </v-card-title>
      <v-expansion-panels flat accordion multiple focusable>
        <v-expansion-panel>
          <v-expansion-panel-header color="#303030">
            <v-row no-gutters>
              <v-col cols="2">Sysctls</v-col>
              <v-col cols="4" class="text--secondary"> (Kernel Options) </v-col>
            </v-row>
          </v-expansion-panel-header>
          <v-expansion-panel-content color="#303030">
            <form>
              <transition-group
                name="slide"
                enter-active-class="animated fadeInLeft fast-anim"
                leave-active-class="animated fadeOutLeft fast-anim"
              >
                <v-row v-for="(item, index) in form.sysctls" :key="index">
                  <v-col>
                    <ValidationProvider
                      name="Name"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        label="Name"
                        v-model="item['name']"
                        :error-messages="errors"
                        :success="valid"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col>
                    <ValidationProvider
                      name="Value"
                      rules="required"
                      v-slot="{ errors, valid }"
                    >
                      <v-text-field
                        label="Value"
                        v-model="item['value']"
                        :error-messages="errors"
                        :success="valid"
                        required
                      ></v-text-field>
                    </ValidationProvider>
                  </v-col>
                  <v-col class="d-flex justify-end" cols="1">
                    <v-btn
                      icon
                      class="align-self-center"
                      @click="removeSysctls(index)"
                    >
                      <v-icon>mdi-minus</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </transition-group>
              <v-row>
                <v-col cols="12" class="d-flex justify-end">
                  <v-btn icon class="align-self-center" @click="addSysctls">
                    <v-icon>mdi-plus</v-icon>
                  </v-btn>
                </v-col>
              </v-row>
            </form>
          </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
          <v-expansion-panel-header color="#303030">
            <v-row no-gutters>
              <v-col cols="2">Capabilities</v-col>
              <v-col cols="4" class="text--secondary">
                (Special Permissions/Capabilities)
              </v-col>
            </v-row></v-expansion-panel-header
          >
          <v-expansion-panel-content color="#303030">
            <form>
              <v-combobox
                v-model="form['cap_add']"
                :items="cap_options"
                label="Add Capabilities"
                multiple
                hide-selected
                clearable
                auto-select-first
                chips
                deletable-chips
              />
            </form>
          </v-expansion-panel-content>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-card>
  </div>
</template>

<script>
import axios from "axios";
import { mapActions, mapMutations } from "vuex";
import { ValidationObserver, ValidationProvider } from "vee-validate";

export default {
  components: {
    ValidationProvider,
    ValidationObserver
  },
  data() {
    return {
      deployStep: 1,
      deploySteps: 4,

      form: {
        name: "",
        image: "",
        restart_policy: "",
        ports: [],
        volumes: [],
        env: [],
        sysctls: [],
        cap_add: []
      },
      isLoading: false,
      cap_options: [
        "SYS_MODULE",
        "SYS_RAWIO",
        "SYS_PACCT",
        "SYS_ADMIN",
        "SYS_NICE",
        "SYS_RESOURCE",
        "SYS_TIME",
        "SYS_TTY_CONFIG",
        "AUDIT_CONTROL",
        "MAC_ADMIN",
        "MAC_OVERRIDE",
        "NET_ADMIN",
        "SYSLOG",
        "DAC_READ_SEARCH",
        "LINUX_IMMUTABLE",
        "NET_BROADCAST",
        "IPC_LOCK",
        "IPC_OWNER",
        "SYS_PTRACE",
        "SYS_BOOT",
        "LEASE",
        "WAKE_ALARM",
        "BLOCK_SUSPEND"
      ]
    };
  },
  methods: {
    ...mapActions({
      readApp: "templates/readApp"
    }),
    ...mapMutations({
      setErr: "snackbar/setErr"
    }),
    addPort() {
      this.form.ports.push({ hport: "", cport: "", proto: "tcp" });
    },
    removePort(index) {
      this.form.ports.splice(index, 1);
    },
    addVolume() {
      this.form.volumes.push({ container: "", bind: "" });
    },
    removeVolume(index) {
      this.form.volumes.splice(index, 1);
    },
    addEnv() {
      this.form.env.push({ label: "", default: "" });
    },
    removeEnv(index) {
      this.form.env.splice(index, 1);
    },
    addSysctls() {
      this.form.sysctls.push({ name: "", value: "" });
    },
    removeSysctls(index) {
      this.form.sysctls.splice(index, 1);
    },
    addCap_add() {
      this.form.cap_add.push("");
    },
    removeCap_add(index) {
      this.form.cap_add.splice(index, 1);
    },
    nextStep(n) {
      if (n === this.deploySteps) {
        // this.deployStep = 1;
        this.submitFormData();
      } else {
        this.deployStep = n + 1;
      }
    },
    submitFormData() {
      const payload = { ...this.form };
      this.isLoading = true;
      const url = `/api/apps/deploy`;
      axios
        .post(url, payload)
        .then(() => {
          this.deployStep = 1;
        })
        .finally(() => {
          this.isLoading = false;
          this.$router.push({ name: "View Applications" });
        });
    },
    async populateForm() {
      const appId = this.$route.params.appId;
      if (appId != null) {
        try {
          const app = await this.readApp(appId);
          this.form = {
            name: app.name || "",
            image: app.image || "",
            restart_policy: app.restart_policy || "",
            ports: app.ports || [],
            volumes: app.volumes || [],
            env: app.env || [],
            sysctls: app.sysctls || [],
            cap_add: app.cap_add || []
          };
        } catch (error) {
          console.error(error, error.response);
          this.setErr(error);
        }
      } else {
        console.log("No app selected");
      }
    }
  },
  async created() {
    await this.populateForm();
  }
};
</script>

<style lang="css" scoped></style>
