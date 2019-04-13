<template>
<div class="dropdown u-ml5"
  :class="{ 'is-active': isActive, 'is-right':isRight, 'is-pulled-right':isPulledRight }">
  <div class="dropdown-trigger">
    <button
      class="button"
      :class="size"
      aria-haspopup="true"
      aria-controls="dropdown-menu"
      @click="isActive = !isActive">
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
        :to="getTransactionsRouterTo($route.query, {category:''})"
        class="dropdown-item"
        :class="{ 'is-active': isEmpty(category) }">
        Select Category
      </router-link>
      <router-link
        v-for="cate in categories" :key="cate.id"
        :to="getTransactionsRouterTo($route.query, {category:cate.id})"
        class="dropdown-item"
        :class="{ 'is-active': !isEmpty(category) && category.id == cate.id }"
        v-text="cate.pathName"></router-link>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: {
    categoryId: {
      type: Number,
      default: 0,
    },
    isRight: {
      type: Boolean,
      default: false,
    },
    isPulledRight: {
      type: Boolean,
      default: false,
    },
    size: {
      type: String,
      default: '',
    },
  },
  data() {
    return {
      isActive: false,
    }
  },
  computed: {
    categories () {
      return this.$store.getters.singleDimCategories
    },
    category () {
      this.isActive = false
      return this.categories.find(item => {
        return item.id === this.categoryId
      })
    },
  },
  created() {
    this.listen(window, 'click', function(e){
      if (!this.$el.contains(e.target)) {
        this.isActive = false
      }
    }.bind(this));
  },
  methods: {
  },
}
</script>
