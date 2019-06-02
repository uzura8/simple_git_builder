<template>
<b-checkbox v-model="isChecked" type="is-info" />
</template>

<script>
export default {
  props: {
    category: {
      type: Object,
      default: {},
    },
  },
  data() {
    return {
      isChecked: false,
    }
  },
  computed: {
  },
  watch: {
    isChecked () {
      this.updateIsMonthly()
    },
  },
  created () {
    this.isChecked = this.category.is_monthly
  },
  methods: {
    updateIsMonthly() {
      if (this.isChecked == this.category.is_monthly) return
      const params = {
        categoryId: this.category.id,
        values: {
          is_monthly: Number(this.isChecked)
        }
      }
      this.$store.dispatch('updateCategory', params)
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },
  }
}
</script>
