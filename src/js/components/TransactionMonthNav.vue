<template>
<nav class="pagination is-centered" role="navigation" aria-label="pagination">
  <a class="pagination-previous" @click="moveMonth(1)">
    <b-icon pack="fas" icon="chevron-left"></b-icon>
  </a>
  <a class="pagination-next" @click="moveMonth(-1)">
    <b-icon pack="fas" icon="chevron-right"></b-icon>
  </a>

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
          <a v-for="item in months" :key="item"
            @click="setMonth(item)"
            class="dropdown-item"
            :class="{ 'is-active': month == item }"
            v-text="item"></a>
        </div>
      </div>
    </div>
  </div>
</nav>
</template>

<script>
import { moment } from '../bootstrap'

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
      months: [],
      updatedValue: '',
      isActiveSelectMonth: false,
    }
  },
  computed: {
    monthIndex () {
      const index = this.months.indexOf(this.value)
      this.isActiveSelectMonth = false
      return index
    },
    month () {
      return this.months[this.monthIndex]
    },
  },
  watch: {
    month (val) {
      this.$emit('input', val)
    },
  },
  created() {
    this.setMonths()
    this.listen(window, 'click', function(e){
      if (!this.$el.contains(e.target)) {
        this.isActiveSelectMonth = false
      }
    }.bind(this));
  },
  methods: {
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
    setMonth: function(month) {
      this.$emit('input', month)
    },
    moveMonth: function(increment = 0) {
      let index = this.monthIndex + increment
      if (index < 0) index = this.months.length - 1
      if (index > this.months.length - 1) index = 0
      this.$emit('input', this.months[index])
    },
  },
}
</script>
