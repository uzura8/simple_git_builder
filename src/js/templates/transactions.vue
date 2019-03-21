<template>
<div>
  <h1 class="title">
    Transactions
  </h1>
  <div v-if="transactions">
    <nav class="pagination is-centered" role="navigation" aria-label="pagination">
      <router-link :to="{path:'/transactions', query:{month: getMonth(1)}}" class="pagination-previous">
        <b-icon pack="fas" icon="chevron-left"></b-icon>
      </router-link>
      <router-link :to="{path:'/transactions', query:{month: getMonth(-1)}}" class="pagination-next">
        <b-icon pack="fas" icon="chevron-right"></b-icon>
      </router-link>
      <div class="pagination-list">
        <div class="dropdown" :class="{ 'is-active': isActiveSelectMonth }">
          <div class="dropdown-trigger">
            <button class="button" aria-haspopup="true" aria-controls="dropdown-menu" @click="isActiveSelectMonth = !isActiveSelectMonth">
              <span>{{ month }}</span>
              <span class="icon is-small">
                <i class="fas fa-angle-down" aria-hidden="true"></i>
              </span>
            </button>
          </div>
          <div class="dropdown-menu" id="dropdown-menu" role="menu">
            <div class="dropdown-content">
              <router-link
                v-for="item in months" :key="item"
                :to="{path:'/transactions', query:{month: item}}"
                class="dropdown-item"
                :class="{ 'is-active': month == item }"
                v-text="item"></router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <table class="table">
      <thead>
        <tr>
          <th>date</th>
          <th>content</th>
          <th>amount</th>
          <th>account</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in transactions" :key="item.id">
          <td>{{item.date | dateFormat('YYYY/MM/DD(ddd)')}}</td>
          <td>{{item.name}}</td>
          <td>{{item.amount | numFormat()}}</td>
          <td>{{item.account_name}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</div>
</template>

<script>
import { moment } from '../bootstrap';

export default {
  data(){
    return {
      months: [],
      isActiveSelectMonth: false,
    }
  },
  computed: {
    monthIndex () {
      let queryMonth = this.$route.query.month;
      if (!queryMonth) queryMonth = this.month = moment().format('YYYY-MM')
      const index = this.months.indexOf(queryMonth)
      this.loadTransactions(this.months[index])
      this.isActiveSelectMonth = false
      return index
    },
    month () {
      return this.months[this.monthIndex]
    },
    transactions () {
      return this.$store.state.transaction.list
      //return this.$store.getters.sortedTransactions
    }
  },
  created() {
    this.setMonths()
  },
  methods: {
    loadTransactions: function(month) {
      this.$store.dispatch('fetchTransactions', { month:month })
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },
    setMonths: function() {
      for (let i = 0, n = 12; i < n; i++) {
        this.months.push(moment().add('months', -1 * i).endOf('month').format('YYYY-MM'))
      }
    },
    getMonth: function(increment = 0) {
      let index = this.monthIndex + increment
      if (index < 0) index = this.months.length - 1
      return this.months[index]
    },
  }
}
</script>
