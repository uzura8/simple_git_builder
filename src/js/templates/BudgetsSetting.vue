<template>
<section>
  <h1 class="title">Budget Management</h1>
  <p class="is-size-5">Set annual budget</p>
  <section>
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <section class="u-mt30">
        <p v-if="!budgets.length">No data</p>
        <section v-else>
          <table class="table u-minw100">
            <thead>
              <tr>
                <th>category</th>
                <th>month</th>
                <th>year</th>
              </tr>
            </thead>
            <tbody>
              <tr class="has-background-white-ter">
                <th>total</th>
                <td class="has-text-weight-semibold">{{ amountTotalByMonth | numFormat()}}</td>
                <td class="has-text-weight-semibold">{{ amountTotal | numFormat()}}</td>
              </tr>
              <budgets-setting-row
                v-for="item in budgets"
                :key="item.category_id"
                :budget="item" />
            </tbody>
          </table>
        </section>
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
    amountTotal () {
      return this.$store.getters.budgetsAmountTotal
    },
    amountTotalByMonth () {
      return this.amountTotal / 12
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
