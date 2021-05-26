<template>
  <div>
    <b-button @click="makeToast()">Show Toast</b-button>
    <b-button @click="makeToast(true)">Show Toast (appended)</b-button>
  </div>
</template>

<script>
  export default {
    methods: {
      makeToast(append = false) {
        this.$bvToast.toast(`This is toast number`, {
          title: 'BootstrapVue Toast',
          autoHideDelay: 50000,
          appendToast: append,
          noCloseButton: true,
        })
      }
    }
  }
</script>