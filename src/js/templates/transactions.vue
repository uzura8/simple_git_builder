<template>
<section>
  <h1 class="title columns is-gapless is-clearfix u-mt0">
    <div class="column">
      Transactions
    </div>
    <div class="column">
      <TransactionCategoryFilter
        v-model="categoryId"
        :isRight="true"
        :isPulledRight="true" />
      <transaction-edit-modal />
    </div>
  </h1>
  <section>
    <TransactionMonthNav v-model="month" />
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <table class="table" v-if="transactions">
        <thead>
          <tr>
            <th>-</th>
            <th>
              <router-link :to="getRouterTo({sort:sortKey == 'date-desc' ? 'date' : 'date-desc'})">
                date
                <b-icon v-if="sortKey == 'date'" pack="fas" icon="caret-down"></b-icon>
                <b-icon v-if="sortKey == 'date-desc'" pack="fas" icon="caret-up"></b-icon>
              </router-link>
            </th>
            <th>content</th>
            <th>
              <router-link :to="getRouterTo({sort:sortKey == 'amount-desc' ? 'amount' : 'amount-desc'})">
                amount
                <b-icon v-if="sortKey == 'amount'" pack="fas" icon="caret-down"></b-icon>
                <b-icon v-if="sortKey == 'amount-desc'" pack="fas" icon="caret-up"></b-icon>
              </router-link>
            </th>
            <th>account</th>
            <th>category</th>
          </tr>
        </thead>
        <tbody>
          <transaction-row
            v-for="item in transactions"
            :key="item.id"
            :transaction="item" />
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
      categoryId: 0,
    }
  },
  computed: {
    sortKey () {
      const acceptKeys = ['date', 'date-desc', 'amount', 'amount-desc']
      const sortKey = this.$route.query.sort
      return util.inArray(sortKey, acceptKeys) ? sortKey : 'date-desc'
    },
    transactions () {
      return this.$store.getters.sortedTransactions(this.categoryId, this.sortKey)
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
    categoryId (val) {
      const params = this.getRouterTo({ 'category':val })
      this.$router.push(params)
    },
    '$route' (to, from) {
      this.loadTransactions(to.query)
    },
  },
  created() {
    this.month = this.validateMonth()
    this.categoryId = this.validateCategoryId()
    let params = {
      month: this.month,
      sortKey: this.sortKey,
    }
    if (this.categoryId) params.category = this.categoryId
    this.loadTransactions(params)
  },
  methods: {
    loadTransactions: function(params) {
      this.$store.dispatch('fetchTransactions', params)
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
      if (!this.isEmpty(this.$route.query.category)) query.category = this.$route.query.category
      if (!this.isEmpty(this.$route.query.sort)) query.sort = this.$route.query.sort
      if (!this.isEmpty(updateQuery)) Object.assign(query, updateQuery);
      let params = { path:'/transactions', query:query }
      return params
    },
    validateMonth: function() {
      if (!this.isEmpty(this.$route.query.month)
        && this.$route.query.month.match(/\d{4}\-\d{2}/) != null) {
        return this.$route.query.month
      }
      return moment().format('YYYY-MM')
    },
    validateCategoryId: function() {
      const categoryId = parseInt(this.$route.query.category)
      return !Number.isNaN(categoryId) ? categoryId : 0
    },
  }
}
</script>
