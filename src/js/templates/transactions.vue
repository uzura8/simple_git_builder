<template>
<section>
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
            :to="getRouterTo({category:''})"
            class="dropdown-item"
            :class="{ 'is-active': isEmpty(category) }">
            Select Category
          </router-link>
          <router-link
            v-for="cate in categories" :key="cate.id"
            :to="getRouterTo({category:cate.id})"
            class="dropdown-item"
            :class="{ 'is-active': !isEmpty(category) && category.id == cate.id }"
            v-text="cate.pathName"></router-link>
        </div>
      </div>
    </div>
  </h1>
  <section>
    <nav class="pagination is-centered" role="navigation" aria-label="pagination">
      <router-link
        class="pagination-previous"
        :to="getRouterTo({month: getMonth(1)})">
        <b-icon pack="fas" icon="chevron-left"></b-icon>
      </router-link>
      <router-link
        class="pagination-next"
        :to="getRouterTo({month: getMonth(-1)})">
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
                :to="getRouterTo({month:item})"
                class="dropdown-item"
                :class="{ 'is-active': month == item }"
                v-text="item"></router-link>
            </div>
          </div>
        </div>
      </div>
    </nav>
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <table class="table" v-if="transactions">
        <thead>
          <tr>
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
          <tr v-for="item in transactions" :key="item.id">
            <td>{{item.date | dateFormat('MM/DD(ddd)')}}</td>
            <td>{{item.name}}</td>
            <td>{{item.amount | numFormat()}}</td>
            <td>{{item.account_name | substr(12)}}</td>
            <td v-text="getCategoryName(item.category_id)"></td>
          </tr>
        </tbody>
      </table>
    </section>
  </section>
</section>
</template>

<script>
import { moment } from '../bootstrap';
import util from '../util';

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
    sortKey () {
      const acceptKeys = ['date', 'date-desc', 'amount', 'amount-desc']
      const sortKey = this.$route.query.sort
      return util.inArray(sortKey, acceptKeys) ? sortKey : 'date-desc';
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
      return this.$store.getters.sortedTransactions(this.categoryId, this.sortKey)
    },
    isLoading () {
      return this.$store.state.common.isLoading
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
    getRouterTo: function(updateQuery = {}) {
      let query = {
        month: this.month,
        category: this.categoryId,
        sort: this.sortKey,
      }
      if (!util.isEmpty(updateQuery)) Object.assign(query, updateQuery);
      let params = { path:'/transactions', query:query }
      return params
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
    getCategoryName: function(categoryId) {
      const category = this.categories.find(item => {
        return item.id === categoryId
      })
      return category.name
    },
  }
}
</script>
