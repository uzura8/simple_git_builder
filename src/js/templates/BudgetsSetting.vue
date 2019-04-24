<template>
<section>
  <h1 class="title">Budget Management</h1>
  <p class="is-size-5">Set annual budget</p>
  <section v-if="!budgets.length" class="u-mt30">
    <p>No data</p>
  </section>
  <section v-else class="u-mt30">
    <div class="box u-sticky">
      <article class="media">
        <div class="media-content">
          <ul>
            <li>
              <label>month</label>
              <span class="has-text-weight-semibold u-ml5">{{ amountTotalByMonth | numFormat()}}</span>
            </li>
            <li>
              <label>year</label>
              <span class="has-text-weight-semibold u-ml5">{{ amountTotal | numFormat()}}</span>
            </li>
          </ul>
        </div>
      </article>
    </div>
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <table class="table u-minw100">
        <thead>
          <tr>
            <th>category</th>
            <th>month</th>
            <th>year</th>
          </tr>
        </thead>
        <tbody>
          <budgets-setting-row
            v-for="item in budgets"
            :key="item.category_id"
            :budget="item" />
        </tbody>
      </table>
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
