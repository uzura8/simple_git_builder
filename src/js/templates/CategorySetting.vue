<template>
<section>
  <h1 class="title">Category Setting</h1>
  <section v-if="!categories.length" class="u-mt30">
    <p>No data</p>
  </section>
  <section v-else class="u-mt30">
    <section class="table-responsive">
      <b-loading :active.sync="isLoading" :is-full-page="false" :canCancel="true"></b-loading>
      <table class="table u-minw100">
        <thead>
          <tr>
            <th>name</th>
            <th>sublabel</th>
          </tr>
        </thead>
        <tbody>
          <category-setting-row
            v-for="item in categories"
            :key="item.id"
            :category="item" />
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
    categories () {
      return this.$store.state.category.list
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
    this.loadCategories()
  },

  methods: {
    loadCategories: function() {
      this.$store.dispatch('fetchCategories', {})
        .catch(err => Promise.reject(err))
        .then(() => {
        })
    },

    createBudget: function() {
    },
  }
}
</script>
