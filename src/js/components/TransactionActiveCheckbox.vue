<template>
<b-checkbox v-model="isActive" type="is-info" />
</template>

<script>
export default {
  props: {
    transaction: {
      type: Object,
      default: {},
    },
  },
  data() {
    return {
      isActive: false,
    }
  },
  computed: {
    isDisabled () {
      return Boolean(this.transaction.is_disabled)
    },
  },
  watch: {
    isActive () {
      if (this.isActive != this.isDisabled) return
      this.updateIsDisabled(!this.isActive)
    },
  },
  created() {
    this.isActive = !this.isDisabled
  },
  methods: {
    updateIsDisabled: function(isDisabled) {
      const params = {
        transactionId: this.transaction.id,
        values: { is_disabled: Number(isDisabled) },
      }
      this.$store.dispatch('updateTransaction', params)
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },
  }
}
</script>
