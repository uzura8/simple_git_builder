<template>
<flat-pickr
  class="input"
  placeholder="Select date"
  :config="config"
  v-model="internalValue"></flat-pickr>
</template>

<script>
import 'flatpickr/dist/flatpickr.css'
import { moment } from '../bootstrap'

export default {
  props: ['value'],
  data () {
    return {
      updatedValue: '',
      config: {
        //altFormat: 'M  j, Y',
        //altInput: true,
        dateFormat: 'Y-m-d',
        //locale: Hindi, // locale for this instance only
      },
    }
  },
  computed: {
    internalValue: {
      get () {
        return this.updatedValue ? this.updatedValue : this.value
      },
      set (newVal) {
        if (this.value !== newVal) this.$emit('input', newVal)
        this.updatedValue = newVal
      }
    }
  },
  created() {
    if (!this.value) {
      this.updatedValue = moment().format('YYYY-MM-DD')
      this.$emit('input', this.updatedValue)
    }
  },
}
</script>
