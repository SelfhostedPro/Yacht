<template lang="html">
  <div id="templates-view" class="templates">
    <h1> Templates </h1>
    <hr/>
    <b-overlay :show="loading" variant="white" rounded="sm">
      <router-view></router-view>
    </b-overlay>
  </div>
</template>
<script>
import { mapState } from "vuex"; 
export default {
  name: "Templates",
  data() {
    return {};
  },
  computed: {
    ...mapState("templates", ["loading"])
  }
};
</script>

<style lang="scss" scoped>
  @import "@/assets/_custom.scss";
  @import "~bootstrap/scss/bootstrap.scss";
  @import '~bootstrap-vue/dist/bootstrap-vue.css';

#templates {
  padding-top: 2em;
  overflow-x: hidden;
  padding-left: 5em;
  padding-right: 2em;
}
</style>
