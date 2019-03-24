<template>
<div>
  <h1 class="title">
    Transactions
    <div class="dropdown is-pulled-right is-right" :class="{ 'is-active': isActiveSelectCate }">
      <div class="dropdown-trigger">
        <button class="button" aria-haspopup="true" aria-controls="dropdown-menu" @click="isActiveSelectCate = !isActiveSelectCate">
          <span v-if="!isEmpty(category)">{{ category.name }}</span>
          <span v-else>Select Category</span>
          <span class="icon is-small">
            <i class="fas fa-angle-down" aria-hidden="true"></i>
          </span>
        </button>
      </div>
      <div class="dropdown-menu" id="dropdown-menu" role="menu">
        <div class="dropdown-content">
          <router-link
            :to="{path:'/transactions', query:{ month:month }}"
            class="dropdown-item"
            :class="{ 'is-active': isEmpty(category) }">
            Select Category
          </router-link>
          <router-link
            v-for="cate in categories" :key="cate.id"
            :to="{path:'/transactions', query:{ month:month, category:cate.id }}"
            class="dropdown-item"
            :class="{ 'is-active': !isEmpty(category) && category.id == cate.id }"
            v-text="cate.pathName"></router-link>
        </div>
      </div>
    </div>
  </h1>
  <div v-if="transactions">
    <nav class="pagination is-centered" role="navigation" aria-label="pagination">
      <router-link
        class="pagination-previous"
        :to="{path:'/transactions', query:{ month: getMonth(1), category:categoryId }}">
        <b-icon pack="fas" icon="chevron-left"></b-icon>
      </router-link>
      <router-link
        class="pagination-next"
        :to="{path:'/transactions', query:{ month: getMonth(-1), category:categoryId }}">
        <b-icon pack="fas" icon="chevron-right"></b-icon>
      </router-link>
      <div class="pagination-list">
        <div class="dropdown" :class="{ 'is-active': isActiveSelectMonth }">
          <div class="dropdown-trigger">
            <button
              class="button"
              aria-haspopup="true"
              aria-controls="dropdown-menu"
              @click="isActiveSelectMonth = !isActiveSelectMonth">
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
                :to="{path:'/transactions', query:{ month: item, category:categoryId }}"
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
      selectedCateId: 0,
      isActiveSelectMonth: false,
      isActiveSelectCate: false,
    }
  },
  computed: {
    monthIndex () {
      let queryMonth = this.$route.query.month;
      if (this.isEmpty(queryMonth)) queryMonth = moment().format('YYYY-MM')
      const index = this.months.indexOf(queryMonth)
      this.loadTransactions(this.months[index])
      this.isActiveSelectMonth = false
      return index
    },
    month () {
      return this.months[this.monthIndex]
    },
    categoryId () {
      const categoryId = parseInt(this.$route.query.category)
      return !Number.isNaN(categoryId) ? categoryId : 0
    },
    category () {
      this.isActiveSelectCate = false
      return this.categories.find(item => {
        return item.id === this.categoryId
      })
    },
    transactions () {
      return this.$store.getters.sortedTransactions(this.categoryId)
    },
    categories () {
      return this.$store.getters.singleDimCategories
    }
  },
  created() {
    this.setMonths()
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
