<template>
<div>
  <h1 class="title">
    Transactions
  </h1>
  <div v-if="transactions">
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
      month: ''
    }
  },
  computed: {
    transactions () {
      return this.$store.state.transaction.list
      //return this.$store.getters.sortedTransactions
    }
  },
  created() {
    if (!this.month) this.month = moment().format('YYYY-MM');
    this.loadTransactions(this.month);
  },
  methods: {
    loadTransactions: function(month) {
      this.$store.dispatch('fetchTransactions', { month:month })
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    }
  }
}
</script>
