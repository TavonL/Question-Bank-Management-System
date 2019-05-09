<template>
  <div id="app">
    <mainIndex></mainIndex>
    <router-view/>
  </div>
</template>

<script>
import MainIndex from '@/components/MainIndex';
export default {
  name: 'App',
  components: { MainIndex }
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 30px;
}
</style>
