<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {},
  methods: {
    a(){
      this.$axios({
        url: 'http://127.0.0.1:8000/admin/',
        method: 'get',
      }).then(response => {
        console.log(response)
      }).catch(error => {
        console.log(error)
      })
    },
  }
}
</script>

<style>

</style>
