<template>
<section>
  <h1 class="title">Budget Management</h1>
  <p class="is-size-5">Set annual budget</p>
  <section>
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <section class="u-mt30">
        <p v-if="!budgets.length">No data</p>
        <table class="table u-minw100" v-else>
          <thead>
            <tr>
              <th>category</th>
              <th>amount</th>
            </tr>
          </thead>
          <tbody>
            <budget-row
              v-for="item in budgets"
              :key="item.category_id"
              :budget="item" />
          </tbody>
        </table>
      </section>
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
      isCreateActive: false,
    }
  },

  computed: {
    budgets () {
      return this.$store.state.budget.list
    },
    isLoading () {
      return this.$store.state.common.isLoading
    },
  },

  watch: {
    //'$route' (to, from) {
    //  this.loadTransactions(to.query)
    //},
  },

  created() {
    this.loadbudgets()
  },

  methods: {
    loadbudgets: function() {
      this.$store.dispatch('fetchBudgets', {})
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },

    createBudget: function() {
    },
  }
}
</script>
