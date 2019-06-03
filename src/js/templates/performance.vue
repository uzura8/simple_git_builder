<template>
<section>

  <h1 class="title">
    Performances
    <router-link
      class="button is-text"
      :to="getRouterTo({month:month}, '/transactions')">
      Transactions
    </router-link>
  </h1>

  <section>
    <div class="tabs">
      <ul>
        <li :class="{ 'is-active': span == 'month'}">
          <a class="u-clickable" @click="span = 'month'">Month</a>
        </li>
        <li :class="{ 'is-active': span == 'year'}">
          <a class="u-clickable" @click="span = 'year'">Year</a>
        </li>
      </ul>
    </div>

    <div class="box">
      <article class="media">
        <div class="media-content">
          <ul>
            <li v-if="isMonthSpan">
              <label>Budget per Month</label>
              <span class="has-text-weight-semibold u-ml5">{{ performancesSums.budget /12 | numFormat }}</span>
            </li>
            <li v-if="isMonthSpan">
              <label>Performance per Month</label>
              <span class="has-text-weight-semibold u-ml5">{{ performancesSums.sum * -1 | numFormat }}</span>
            </li>
            <li v-if="isYearSpan">
              <label>Budget Total</label>
              <span class="has-text-weight-semibold u-ml5">{{ performancesSums.budget | numFormat }}</span>
            </li>
            <li v-if="isYearSpan">
              <label>Performance Total</label>
              <span class="has-text-weight-semibold u-ml5">{{ performancesSums.sum_year * -1 | numFormat }}</span>
              <span class="u-ml5">({{ Math.floor(performancesSums.sum_year * -1 / performancesSums.budget * 100 * 10) / 10 }} %)</span>
            </li>
            <li v-if="isYearSpan">
              <label>Past Month %</label>
              <span class="has-text-weight-semibold u-ml5">{{ Math.floor(monthNum / 12 * 100 * 10) / 10 }}</span>
            </li>
          </ul>
        </div>
      </article>
    </div>

    <TransactionMonthNav v-model="month" />

    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <table class="table" v-if="performances">
        <thead>
          <tr>
            <th>-</th>
            <th>Category</th>
            <th v-if="isMonthSpan">Budget</th>
            <th v-if="isMonthSpan">Perf</th>
            <th v-if="isMonthSpan">Diff</th>
            <th v-if="isMonthSpan">%</th>
            <th v-if="isMonthSpan">Budget Day</th>
            <th v-if="isMonthSpan">Perf Day</th>
            <th v-if="isYearSpan">Budget Year</th>
            <th v-if="isYearSpan">Perf Year</th>
            <th v-if="isYearSpan">%</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in performances"
            :key="item.id"
            :class="{ 'has-background-grey-lighter': inArray(item.id, disabledCategoryIds) }">
            <td>
              <b-checkbox v-model="disabledCategoryObj[item.id]" />
            </td>
            <td>
              <router-link
                class="button is-text"
                :to="getRouterTo({category:item.id}, '/transactions')"
                 v-text="getCategoryLabel(item)" />
            </td>
            <td v-if="isMonthSpan">{{ item.budget / 12 | numFormat }}</td>
            <td v-if="isMonthSpan">{{ item.sum * -1 | numFormat }}</td>
            <td v-if="isMonthSpan">{{ item.budget / 12 - item.sum * -1 | numFormat }}</td>
            <td v-if="isMonthSpan" v-text="calcBudgetRate(item.sum, item.budget)"></td>
            <td v-if="isMonthSpan">{{ item.budget / 12 / daysInMonth | numFormat }}</td>
            <td v-if="isMonthSpan">{{ item.sum * -1 / progressDays | numFormat }}</td>
            <td v-if="isYearSpan">{{ item.budget | numFormat }}</td>
            <td v-if="isYearSpan">{{ item.sum_year * -1 | numFormat }}</td>
            <td v-if="isYearSpan" v-text="calcBudgetRate(item.sum_year, item.budget, true)"></td>
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
      span: '',
      disabledCategoryObj: {},
    }
  },

  computed: {
    performances () {
      return this.$store.state.performance.list
    },

    performancesSums () {
      return this.$store.getters.performancesSums(this.disabledCategoryIds)
    },

    disabledCategoryIds () {
      return Object.keys(this.disabledCategoryObj)
        .filter(key => this.disabledCategoryObj[key] === true)
        .map(e => parseInt(e))
    },

    isLoading () {
      return this.$store.state.common.isLoading
    },

    daysInMonth () {
      const month_end_dt = moment(this.month).endOf('month')
      return month_end_dt.daysInMonth()
    },

    progressDays () {
      const month_end_dt = moment(this.month).endOf('month')
      if (month_end_dt.isAfter()) {
        return moment().date()
      }
      return month_end_dt.daysInMonth()
    },

    monthNum () {
      const items = this.month.split('-')
      return Number(items[1])
    },

    isMonthSpan () {
      return this.span == 'month'
    },

    isYearSpan () {
      return this.span == 'year'
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
    this.span = this.validateSpan()
    const params = {
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

    getRouterTo: function(updateQuery = {}, path = '/performance') {
      let query = {}
      if (!this.isEmpty(this.$route.query.month)) query.month = this.$route.query.month
      if (!this.isEmpty(this.$route.query.span)) query.span = this.$route.query.span
      if (!this.isEmpty(updateQuery)) Object.assign(query, updateQuery);
      let params = { path:path, query:query }
      return params
    },

    calcBudgetRate: function(amount, budget, isYear = false) {
      if (!budget) return ''
      const month = isYear ? 1 : 12
      return Math.floor(amount * -1 / (budget / month) * 100 * 10) / 10
    },

    validateMonth: function() {
      if (!this.isEmpty(this.$route.query.month)
        && this.$route.query.month.match(/\d{4}\-\d{2}/) != null) {
        return this.$route.query.month
      }
      return moment().format('YYYY-MM')
    },

    validateSpan: function() {
      const accepts = ['month', 'year']
      if (this.isEmpty(this.$route.query.span)) return 'month'
      if (!this.inArray(this.$route.query.span, accepts)) return 'month'
      return this.$route.query.span
    },
  }
}
</script>
