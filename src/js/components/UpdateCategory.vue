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
        v-if="!isParentCateOnly || isParentCateOnly && (cate.isParent || categoryId == cate.id)"
        class="dropdown-item u-clickable"
        :class="{ 'is-active': !isEmpty(category) && categoryId == cate.id, 'is-loading': isLoading }"
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
    isParentCateOnly () {
      return this.siteConfig('IS_PARENT_CATEGORY_ONLY')
    },
    category () {
      return this.categories.find(item => {
        return item.id === this.categoryId
      })
    },
    categories () {
      return this.$store.getters.singleDimCategories()
    },
    isLoading () {
      return this.$store.state.common.isLoading
    },
    btnSizeClass () {
      const accepts = ['small', 'medium', 'large']
      if (this.isEmpty(this.btnSize)) return ''
      if (!this.inArray(this.btnSize, accepts)) return ''
      return `is-${this.btnSize}`
    },
  },
  watch: {
  },
  created() {
    this.listen(window, 'click', function(e){
      if (!this.$el.contains(e.target)) {
        this.isActive = false
      }
    }.bind(this));
  },
  methods: {
    updateCategory: function(categoryId) {
      this.$store.dispatch('setIsLoading', true)
      if (this.category.id == categoryId) {
        this.isActive = false
        this.$store.dispatch('setIsLoading', false)
        return false
      }
      const params = {
        transactionId: this.transactionId,
        values: {
          category_id: categoryId
        }
      }
      this.$store.dispatch('updateTransaction', params)
          .catch(err => {
            this.$store.dispatch('setIsLoading', false)
            this.$toast.open({
              message: err.message,
              type: 'is-danger',
              duration: 5000,
              position: 'is-bottom',
            })
          })
        .then(() => {
          this.$emit('input', categoryId)
          this.$store.dispatch('setIsLoading', false)
          this.isActive = false
        })
    },
  }
}
</script>
