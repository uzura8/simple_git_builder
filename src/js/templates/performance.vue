<template>
<section>
  <h1 class="title">Performances</h1>
  <section>
    <TransactionMonthNav v-model="month" />
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <table class="table" v-if="performances">
        <thead>
          <tr>
            <th>Category</th>
            <th>Budget</th>
            <th>Performance</th>
            <th>Diff</th>
            <th>%</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in performances" :key="item.id">
            <td>{{ item.name }}</td>
            <td>{{ item.budget / 12 | numFormat }}</td>
            <td>{{ item.sum * -1 | numFormat }}</td>
            <td v-text="calcBudgetRate(item.sum, item.budget)"></td>
          </tr>
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
      month: '',
    }
  },

  computed: {
    performances () {
      return this.$store.state.performance.list
    },

    isLoading () {
      return this.$store.state.common.isLoading
    },
  },

  watch: {
    month (val) {
      const params = this.getRouterTo({ 'month':val })
      this.$router.push(params)
    },

    '$route' (to, from) {
      this.loadPerformances(to.query)
    },
  },

  created() {
    this.month = this.validateMonth()
    let params = {
      month: this.month,
    }
    this.loadPerformances(params)
  },

  methods: {
    loadPerformances: function(params) {
      this.$store.dispatch('fetchPerformances', params)
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

    getRouterTo: function(updateQuery = {}) {
      let query = {}
      if (!this.isEmpty(this.$route.query.month)) query.month = this.$route.query.month
      if (!this.isEmpty(updateQuery)) Object.assign(query, updateQuery);
      let params = { path:'/performance', query:query }
      return params
    },

    calcBudgetRate: function(amount, budget) {
      if (!budget) return ''
      return Math.floor(amount * -1 / (budget / 12) * 100 * 10) / 10
    },

    validateMonth: function() {
      if (!this.isEmpty(this.$route.query.month)
        && this.$route.query.month.match(/\d{4}\-\d{2}/) != null) {
        return this.$route.query.month
      }
      return moment().format('YYYY-MM')
    },
  }
}
</script>
