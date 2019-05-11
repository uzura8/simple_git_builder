<template>
<b-dropdown
  aria-role="menu"
  v-model="internalValue"
  :class="{ 'is-right':isRight, 'is-pulled-right':isPulledRight }">
  <button class="button" type="button" slot="trigger" :class="btnSizeClass">
    <template v-if="updatedValue">
      <span>{{ account.name }}</span>
    </template>
    <template v-else>
      <span>Select Account</span>
    </template>
    <b-icon icon="caret-down" pack="fas"></b-icon>
  </button>

  <b-dropdown-item
    v-for="account in accounts"
    :key="account.code"
    :value="account.code"
    :class="{ 'is-active': updatedValue == account.id }"
     aria-role="menuitem">
    {{ account.name }}
  </b-dropdown-item>
</b-dropdown>
</template>

<script>
export default {
  props: {
    value: {
      type: String,
      default: '',
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
    account () {
      return this.accounts.find(item => {
        return item.code === this.updatedValue
      })
    },

    accounts () {
      return this.$store.state.account.list
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
  created() {
    this.updatedValue = this.value
    this.$emit('input', this.updatedValue)
  },
}
</script>
