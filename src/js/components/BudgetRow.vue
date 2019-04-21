<template>
<tr>
  <td>{{budget.category_name}}</td>
  <td v-if="isEditable">
    <b-field grouped>
        <b-input
          placeholder="Please input amount"
          type="number"
          icon="yen-sign"
          icon-pack="fas"
          name="amount"
          ref="amount"
          expanded
          v-model="amount"
          @focus="$event.target.select()"
          @keydown.enter.native="updateAmount"
          @keyup.esc.native="cancel" />
      <p class="control">
        <button class="button is-info" @click="updateAmount">OK</button>
      </p>
    </b-field>
  </td>
  <td v-else
    @click="changeEditable">{{amount | numFormat()}}</td>
</tr>
</template>

<script>
export default {
  props: {
    budget: {
      type: Object,
      default: {},
    },
  },

  data () {
    return {
      isEditable: false,
      onFocus: false,
      tmp: 0,
      amount: 0,
    }
  },

  computed: {
  },

  watch: {
  },

  created() {
    this.amount = this.budget.amount
  },

  methods: {
    changeEditable() {
      this.tmp = this.amount
      this.isEditable = !this.isEditable
      this.$nextTick(() => this.$refs.amount.focus())
    },

    updateAmount() {
      if (this.amount == this.tmp) {
        this.isEditable = false
        return
      }
      const params = {
        categoryId: this.budget.category_id,
        values: {
          amount: this.amount
        }
      }
      this.$store.dispatch('updateBudget', params)
        .catch(err => Promise.reject(err))
        .then(() => {
          this.isEditable = false
          this.tmp = 0
        })
    },

    cancel() {
      this.amount = this.tmp
      this.isEditable = false
    },
  },
}
</script>
