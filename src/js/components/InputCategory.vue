<template>
<b-dropdown
  aria-role="menu"
  v-model="internalValue"
  :class="{ 'is-right':isRight, 'is-pulled-right':isPulledRight }">
  <button class="button" type="button" slot="trigger" :class="btnSizeClass">
    <template v-if="updatedValue">
      <span>{{ category.name }}</span>
    </template>
    <template v-else>
      <span>Select Category</span>
    </template>
    <b-icon icon="caret-down" pack="fas"></b-icon>
  </button>

  <b-dropdown-item
    v-for="cate in categories"
    :key="cate.id"
    :value="cate.id"
    :class="{ 'is-active': updatedValue == cate.id }"
     aria-role="menuitem">
    {{ cate.pathName }}
  </b-dropdown-item>
</b-dropdown>
</template>

<script>
export default {
  props: {
    value: {
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
      updatedValue: 0,
      isActive: false,
    }
  },
  computed: {
    category () {
      return this.categories.find(item => {
        return item.id === this.updatedValue
      })
    },
    categories () {
      return this.$store.getters.singleDimCategories
    },
    btnSizeClass () {
      const accepts = ['is-small', 'is-medium', 'is-large']
      if (this.isEmpty(this.size)) return ''
      if (!this.inArray(this.size, accepts)) return ''
      return this.size
    },
    internalValue: {
      get () {
        return this.updatedValue ? this.updatedValue : this.value
      },
      set (newVal) {
        if (this.value !== newVal) this.$emit('input', newVal)
        this.updatedValue = newVal
      }
    },
  },
  watch: {
    //value (val) {
    //},
  },
  created() {
    this.updatedValue = this.value
    this.$emit('input', this.updatedValue)
  },
}
</script>
