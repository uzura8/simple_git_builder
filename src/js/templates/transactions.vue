<template>
<section>
  <h1 class="title columns is-gapless is-clearfix u-mt0">
    <div class="column">
      Transactions
    </div>
    <div class="column">
      <TransactionCategoryFilter
        :categoryId="categoryId"
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
              <router-link :to="getTransactionsRouterTo($route.query, {sort:sortKey == 'date-desc' ? 'date' : 'date-desc'})">
                date
                <b-icon v-if="sortKey == 'date'" pack="fas" icon="caret-down"></b-icon>
                <b-icon v-if="sortKey == 'date-desc'" pack="fas" icon="caret-up"></b-icon>
              </router-link>
            </th>
            <th>content</th>
            <th>
              <router-link :to="getTransactionsRouterTo($route.query, {sort:sortKey == 'amount-desc' ? 'amount' : 'amount-desc'})">
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
      selectedCateId: 0,
    }
  },
  computed: {
    sortKey () {
      const acceptKeys = ['date', 'date-desc', 'amount', 'amount-desc']
      const sortKey = this.$route.query.sort
      return util.inArray(sortKey, acceptKeys) ? sortKey : 'date-desc'
    },
    categoryId () {
      const categoryId = parseInt(this.$route.query.category)
      return !Number.isNaN(categoryId) ? categoryId : 0
    },
    transactions () {
      return this.$store.getters.sortedTransactions(this.categoryId, this.sortKey)
    },
    isLoading () {
      return this.$store.state.common.isLoading
    },
    categories () {
      return this.$store.getters.singleDimCategories
    }
  },
  watch: {
    month (val) {
      const params = this.getTransactionsRouterTo(this.$route.query, { 'month':val })
      this.$router.push(params)
    },
    '$route' (to, from) {
      this.loadTransactions(to.query.month)
    },
  },
  created() {
    if (this.isEmpty(this.month)) {
      this.month = this.$route.query.month ?
        this.$route.query.month : moment().format('YYYY-MM')
    }
    this.loadCategories()
  },
  methods: {
    loadTransactions: function(month) {
      this.$store.dispatch('fetchTransactions', { month:month })
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },
    loadCategories: function() {
      this.$store.dispatch('fetchCategories')
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },
  }
}
</script>
