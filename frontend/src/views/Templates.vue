<template lang="html">
  <div id="templates-view" class="templates">
    <h1> Templates </h1>
    <hr/>
    <router-view></router-view>
  </div>
</template>
<script>

export default {
  name: "Templates",
  data() {
    return {
    };
  },
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
