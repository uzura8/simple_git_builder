<template>
<span>
  <button
    class="button is-pulled-right"
    :class="[buttonSize, isNew ? 'is-info' : '']"
    @click="isModalActive = true">
    <b-icon pack="fas" class="is-small" :icon="isNew ? 'plus' : 'edit'"></b-icon>
    <span v-if="dispButtonLabel" v-text="isNew ? 'Create' : 'Update'"></span>
  </button>
  <b-modal :active.sync="isModalActive" has-modal-card>
    <div class="modal-card" style="width: auto">
      <header class="modal-card-head">
        <p class="modal-card-title"
          v-text="isNew ? 'Create Transaction' : 'Update Transaction'"></p>
      </header>
      <section class="modal-card-body">
        <b-field label="Preset">
          <transaction-preset-dropdown v-model="presetId" name="presetId" />
        </b-field>

        <b-field label="Date"
          :type="{'is-danger': errors.date}"
          :message="errors.date">
          <input-date
            v-model="date"
            required
            name="date" />
        </b-field>

        <b-field label="Content"
          :type="{'is-danger': errors.name}"
          :message="errors.name">
          <b-input
            type="text"
            placeholder="Please input content"
            required
            name="name"
            v-model="name" />
        </b-field>

        <b-field label="Amount"
          :type="{'is-danger': errors.amount}"
          :message="errors.amount">
          <b-input
            placeholder="Please input amount"
            type="number"
            required
            icon="yen-sign"
            icon-pack="fas"
            name="amount"
            v-model="amount" />
        </b-field>

        <b-field label="Category"
          :type="{'is-danger': errors.category_id}"
          :message="errors.category_id">
          <input-category
            name="category_id"
            v-model="category_id" />
        </b-field>

        <b-field label="Account"
          :type="{'is-danger': errors.account_code}"
          :message="errors.account_code">
          <input-account
            name="account_code"
            v-model="account_code" />
        </b-field>

      </section>
      <footer class="modal-card-foot">
        <button class="button" type="button" @click="isModalActive = false">Close</button>
        <button
          class="button is-primary"
          v-text="isNew ? 'Create' : 'Update'"
          @click="save()"></button>
      </footer>
    </div>
  </b-modal>
</span>
</template>

<script>

export default {
  props: {
    transactionId: {
      type: Number,
    },
    updateCategoryId: {
      type: Number,
      default: 0,
    },
    buttonSize: {
      type: String,
      default: '',
    },
    dispButtonLabel: {
      type: Boolean,
      default: true,
    },
  },

  data() {
    return {
      isModalActive: false,
      name: '',
      date: '',
      amount: 0,
      category_id: 0,
      account_code: 'manual',
      presetId: 0,
      errors: {
        name: '',
        amount: '',
        date: '',
        category_id: '',
        account_code: '',
      },
    }
  },

  computed: {
    transaction () {
      return this.$store.getters.transaction(this.transactionId)
    },
    isNew () {
      return this.isEmpty(this.transaction)
    },
    updatedValues () {
      const keys = ['name', 'date', 'amount', 'account_code', 'category_id']
      let isUpdated = false
      let values = {}
      for (let i = 0, n = keys.length; i < n; i++) {
        let key = keys[i]
        if (this.transaction[key] != this[key]) {
          values[key] = this[key]
          isUpdated = true
        }
      }
      if (!isUpdated) return false
      return values
    },
  },

  watch: {
    updateCategoryId (val) {
      this.category_id = val
    },
    presetId (val) {
      if (!val) return
      const preset = this.$store.getters.transactionPreset(val)
      this.name = preset.name
      this.amount = preset.amount
      this.category_id = preset.category_id
      this.account_code = preset.account_code
    },
  },

  created() {
    if (!this.isNew) {
      this.setValues()
    }
  },

  methods: {
    save: function() {
      if (this.validateAll() == false) {
        this.$toast.open({
          message: 'Form is not valid! Please check the fields.',
          type: 'is-danger',
          position: 'is-bottom'
        })
      } else {
        const values = {
          name: this.name,
          date: this.date,
          amount: this.amount,
          category_id: this.category_id,
          account_code: this.account_code,
        }
        if (this.isNew) {
          this.$store.dispatch('createTransaction', values)
            .catch(err => {
              this.$toast.open({
                message: err.message,
                type: 'is-danger',
                duration: 5000,
                position: 'is-bottom',
              })
            })
            .then(() => {
              this.isModalActive = false
              this.$toast.open({
                message: 'Created transaction.',
                type: 'is-success'
              })
              this.resetValues()
            })
        } else if (this.updatedValues) {
          const params = {
            transactionId: this.transaction.id,
            values: this.updatedValues,
          }
          this.$store.dispatch('updateTransaction', params)
            .catch(err => {
              this.$toast.open({
                message: err.message,
                type: 'is-danger',
                duration: 5000,
                position: 'is-bottom',
              })
            })
            .then(() => {
              this.isModalActive = false
              this.$toast.open({
                message: 'Updated transaction.',
                type: 'is-success'
              })
            })
            this.resetValues()
        }
      }
    },

    setValues: function() {
      this.name = this.transaction.name
      this.date = this.transaction.date
      this.amount = this.transaction.amount
      this.category_id = this.transaction.category_id
      this.account_code = this.transaction.account_code
    },

    resetValues: function() {
      this.name = ''
      this.date = ''
      this.amount = 0
      this.category_id = 0
      this.account_code = ''
      this.presetId = 0
    },

    resetErros: function() {
      this.errors.name = ''
      this.errors.date = ''
      this.errors.amount = ''
      this.errors.category_id = ''
      this.errors.account_code = ''
    },

    validateAll: function() {
      this.resetErros()
      let isError = false
      if (!this.name) {
        this.errors.name = 'Please input'
        isError = true
      }
      if (!this.date) {
        this.errors.date = 'Please input'
        isError = true
      }
      if (!this.category_id) {
        this.errors.category_id = 'Please select'
        isError = true
      }
      return !isError
    },
  }
}
</script>

