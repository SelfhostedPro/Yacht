<template lang="html">
  <div id="templates-view" class="templates">
    <h1>Templates</h1>
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

<style lang="css" scoped>
#templates {
  padding-top: 1em;
  overflow-x: hidden;
  padding-left: 5em;
  padding-right: 2em;
}
</style>
