<template lang="html">
  <div class="apps-form">
    <v-stepper v-model="deployStep">
      <v-stepper-header>
        <v-stepper-step step="1">
          Basics
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="2">
          Ports
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="3">
          Volumes
        </v-stepper-step>
        <v-divider></v-divider>
        <v-stepper-step step="4">
          Environment
        </v-stepper-step>
      </v-stepper-header>

      <v-stepper-items>
        <v-stepper-content step="1">
          <form>
            <v-text-field
              label="Title"
              placeholder="My Container"
              v-model="form.title"
            ></v-text-field>
            <v-text-field
              label="Image"
              placeholder="image:my-image"
              v-model="form.image"
            ></v-text-field>
            <v-select
              :items="['always', 'on-failure', 'unless-stopped']"
              label="Restart Policy"
              v-model="form['restart_policy']"
            ></v-select>
          </form>
          <v-btn color="primary" @click="nextStep(1)">
            Continue
          </v-btn>
        </v-stepper-content>

        <v-stepper-content step="2">
          <form>
            <v-row v-for="(item, index) in form.ports" :key="index">
              <v-col>
                <v-text-field
                  type="number"
                  label="Container"
                  placeholder="80"
                  min=0
                  max=65535
                  v-model="item['cport']"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  type="number"
                  label="Host"
                  placeholder="80"
                  min=0
                  max=65535
                  v-model="item['hport']"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-select
                  :items="['tcp', 'udp']"
                  label="Protocol"
                  v-model="item['proto']"
                ></v-select>
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
            <v-row>
              <v-col cols="12" class="d-flex justify-end">
                <v-btn icon class="align-self-center" @click="addPort">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </form>
          <v-btn color="primary" @click="nextStep(2)">
            Continue
          </v-btn>
        </v-stepper-content>

        <v-stepper-content step="3">
          <form>
            <v-row v-for="(item, index) in form.volumes" :key="index">
              <v-col>
                <v-text-field
                  label="Container"
                  placeholder="/share"
                  v-model="item['host']"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  label="Host"
                  placeholder="/yacht/image/share"
                  v-model="item['bind']"
                ></v-text-field>
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
            <v-row>
              <v-col cols="12" class="d-flex justify-end">
                <v-btn icon class="align-self-center" @click="addVolume">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </form>
          <v-btn color="primary" @click="nextStep(3)">
            Continue
          </v-btn>
        </v-stepper-content>

        <v-stepper-content step="4">
          <form>
            <v-row v-for="(item, index) in form.env" :key="index">
              <v-col>
                <v-text-field
                  label="Label"
                  v-model="item['label']"
                ></v-text-field>
              </v-col>
              <v-col>
                <v-text-field
                  label="Host"
                  v-model="item['default']"
                ></v-text-field>
              </v-col>
              <v-col class="d-flex justify-end" cols="1">
                <v-btn icon class="align-self-center" @click="removeEnv(index)">
                  <v-icon>mdi-minus</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" class="d-flex justify-end">
                <v-btn icon class="align-self-center" @click="addEnv">
                  <v-icon>mdi-plus</v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </form>
          <v-btn color="primary" @click="nextStep(4)">
            Continue
          </v-btn>
        </v-stepper-content>

      </v-stepper-items>
    </v-stepper>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      deployStep: 1,
      deploySteps: 4,

      form: {
        title: "My Container",
        image: "image:my-image",
        restart_policy: "unless-stopped",
        ports: [
          {
            cport: "80",
            hport: "80",
            proto: "tcp"
          }
        ],
        volumes: [
          {
            container: "/share",
            bind: "/yacht/image/share"
          }
        ],
        env: [
          {
            label: "JAVA_OPTS",
            default: "-IDK WHAT THE HELL"
          }
        ]
      }
    };
  },
  methods: {
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
    nextStep(n) {
      if (n === this.deploySteps) {
        this.deployStep = 1;
        this.submitFormData();
      } else {
        this.deployStep = n + 1;
      }
    },
    submitFormData() {
      const payload = { ...this.form };
      console.log("submit", payload);
      const appId = this.$route.params.appId;
      const url = `/api/apps/${appId}/deploy`;
      axios.post(url, payload).then(response => {
        console.log(response);
      });
    }
  },
  created() {
    // const appId = this.$router.params.appId;
    // this.readApp(appId);
  }
};
</script>

<style lang="css" scoped></style>
