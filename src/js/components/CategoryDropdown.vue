<template>
<div class="dropdown"
  :class="{ 'is-active': isActive, 'is-right':isRight, 'is-pulled-right':isPulledRight }">
  <div class="dropdown-trigger">
    <button
      class="button"
      aria-haspopup="true"
      aria-controls="dropdown-menu"
      :class="btnSizeClass"
      @click="isActive = !isActive">
      <span v-if="!isEmpty(category)">{{ category.name }}</span>
      <span v-else>Select Category</span>
      <span class="icon">
        <i class="fas fa-angle-down" aria-hidden="true"></i>
      </span>
    </button>
  </div>
  <div class="dropdown-menu" id="dropdown-menu" role="menu">
    <div class="dropdown-content">
      <a v-for="cate in categories" :key="cate.id"
        class="dropdown-item u-clickable"
        :class="{ 'is-active': !isEmpty(category) && categoryId == cate.id }"
        @click="updateCategory(cate.id)">{{ cate.pathName }}</a>
    </div>
  </div>
</div>
</template>

<script>
export default {
  props: {
    transactionId: {
      type: Number,
      default: 0,
    },
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
    btnSize: {
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
    category () {
      return this.categories.find(item => {
        return item.id === this.categoryId
      })
    },
    categories () {
      return this.$store.getters.singleDimCategories
    },
    btnSizeClass () {
      const accepts = ['small', 'medium', 'large']
      if (this.isEmpty(this.btnSize)) return ''
      if (!this.inArray(this.btnSize, accepts)) return ''
      return `is-${this.btnSize}`
    },
  },
  watch: {
    //selectedKey () {
    //},
  },
  created() {
  },
  methods: {
    updateCategory: function(categoryId) {
      if (this.category.id == categoryId) {
        this.isActive = false
        return false
      }
      const params = {
        transactionId: this.transactionId,
        values: {
          category_id: categoryId
        }
      }
      this.$store.dispatch('updateTransaction', params)
        .catch(err => Promise.reject(err))
        .then(() => {
          this.isActive = false
        })
    },
  }
}
</script>
