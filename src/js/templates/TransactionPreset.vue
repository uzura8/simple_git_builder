<template>
<section>
  <h1 class="title columns is-gapless is-clearfix u-mt0">
    <div class="column">Transaction Presets</div>
    <div class="column">
      <transaction-preset-edit-modal />
    </div>
  </h1>
  <section>
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <table class="table" v-if="presets.length">
        <thead>
          <tr>
            <th>-</th>
            <th>name</th>
            <th>content</th>
            <th>amount</th>
            <th>category</th>
            <th>account</th>
            <th>-</th>
          </tr>
        </thead>
        <tbody>
          <transaction-preset-row
            v-for="item in presets"
            :key="item.id"
            :preset="item" />
        </tbody>
      </table>
      <p v-else>No data.</p>
    </section>
  </section>
</section>
</template>

<script>
import { moment } from '../bootstrap'
import util from '../util'

export default {
  data(){
    return {
    }
  },

  computed: {
    presets () {
      return this.$store.state.transactionPreset.list
    },

    isLoading () {
      return this.$store.state.common.isLoading
    },
  },

  watch: {
  },

  created() {
    this.loadPresets()
    this.loadCategories()
    this.loadAccounts()
  },

  methods: {
    loadPresets: function(params = {}) {
      this.$store.dispatch('fetchTransactionPresets', params)
        .catch(err => {
          this.$toast.open({
            message: err.message,
            type: 'is-danger',
            duration: 5000,
            position: 'is-bottom',
          })
        })
        .then(() => {
        })
    },

    loadCategories: function() {
      this.$store.dispatch('fetchCategories')
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },

    loadAccounts: function() {
      this.$store.dispatch('fetchAccounts')
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },
  }
}
</script>
