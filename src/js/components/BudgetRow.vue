<template>
<tr>
  <td>{{budget.category_name}}</td>
  <td>{{amountByMonth | numFormat()}}</td>
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
          @blur="blurInput"
          @focus="focus($event.target)"
          @keydown.enter.native="updateAmount"
          @keyup.esc.native="cancel" />
      <p class="control">
        <button class="button is-info" @mousedown="updateAmount">OK</button>
      </p>
    </b-field>
  </td>
  <td v-else @click="changeEditable">
    <span>{{amount | numFormat()}}</span>
    <b-icon icon="edit" pack="fas" size="is-small" class="is-pulled-right has-text-grey-lighter" />
  </td>
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
      isFocus: false,
      isUpdated: false,
      tmp: 0,
      amount: 0,
    }
  },

  computed: {
    amountByMonth () {
      return this.amount / 12
    },
  },

  watch: {
  },

  created() {
    this.amount = this.budget.amount
  },

  methods: {
    changeEditable() {
      this.tmp = this.amount
      this.isEditable = true
      this.$nextTick(() => this.$refs.amount.focus())
    },

    updateAmount() {
      this.isUpdated = true
      if (this.amount == this.tmp) {
        this.reseEditable()
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
          this.reseEditable(false)
          this.tmp = 0
        })
    },

    focus(eventTarget) {
      eventTarget.select()
      this.isFocus = true
    },

    blurInput() {
      if (!this.isFocus) return
      if (this.isUpdated) return
      this.cancel()
    },

    cancel() {
      this.reseEditable()
    },

    reseEditable(isRecoverAmount = true) {
      if (isRecoverAmount) this.amount = this.tmp
      this.isFocus = false
      this.isEditable = false
      this.isUpdated = false
    },
  },
}
</script>
