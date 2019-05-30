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
          v-text="isNew ? 'Create Preset' : 'Update Preset'"></p>
      </header>
      <section class="modal-card-body">

        <b-field label="Name"
          :type="{'is-danger': errors.name}"
          :message="errors.name">
          <b-input
            type="text"
            placeholder="Please input name"
            required
            name="name"
            v-model="name" />
        </b-field>

        <b-field label="Content"
          :type="{'is-danger': errors.transaction_name}"
          :message="errors.transaction_name">
          <b-input
            type="text"
            placeholder="Please input content"
            name="transaction_name"
            v-model="transaction_name" />
        </b-field>

        <b-field label="Amount"
          :type="{'is-danger': errors.amount}"
          :message="errors.amount">
          <b-input
            placeholder="Please input amount"
            type="number"
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
          :class="{ 'is-loading': isLoading }"
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
    presetId: {
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
      transaction_name: '',
      amount: 0,
      category_id: 0,
      account_code: '',
      errors: {
        name: '',
        transaction_name: '',
        amount: '',
        category_id: '',
        account_code: '',
      },
    }
  },

  computed: {
    preset () {
      return this.$store.getters.transactionPreset(this.presetId)
    },
    isLoading () {
      return this.$store.state.common.isLoading
    },
    isNew () {
      return this.isEmpty(this.preset)
    },
    updatedValues () {
      const keys = ['name', 'transaction_name', 'amount', 'account_code', 'category_id']
      let isUpdated = false
      let values = {}
      for (let i = 0, n = keys.length; i < n; i++) {
        let key = keys[i]
        if (this.preset[key] != this[key]) {
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
  },
  created() {
    if (!this.isNew) {
      this.setValues()
    }
  },

  methods: {
    save: function() {
      this.$store.dispatch('setIsLoading', true)
      if (this.validateAll() == false) {
        this.$store.dispatch('setIsLoading', false)
        this.$toast.open({
          message: 'Form is not valid! Please check the fields.',
          type: 'is-danger',
          position: 'is-bottom'
        })
      } else {
        const values = {
          name: this.name,
          transaction_name: this.transaction_name,
          amount: this.amount,
          category_id: this.category_id,
          account_code: this.account_code,
        }
        if (this.isNew) {
          this.$store.dispatch('createTransactionPreset', values)
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
              this.$store.dispatch('setIsLoading', false)
              this.isModalActive = false
              this.$toast.open({
                message: 'Created preset.',
                type: 'is-success'
              })
              this.resetValues()
            })
        } else if (!this.isEmpty(this.updatedValues)) {
          const params = {
            transactionPresetId: this.preset.id,
            values: this.updatedValues,
          }
          this.$store.dispatch('updateTransactionPreset', params)
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
              this.$store.dispatch('setIsLoading', false)
              this.isModalActive = false
              this.$toast.open({
                message: 'Updated preset.',
                type: 'is-success'
              })
            })
        } else {
          this.$store.dispatch('setIsLoading', false)
          this.isModalActive = false
        }
      }
    },

    setValues: function() {
      this.name = this.preset.name
      this.transaction_name = this.preset.transaction_name
      this.amount = this.preset.amount
      this.category_id = this.preset.category_id
      this.account_code = this.preset.account_code
    },

    resetValues: function() {
      this.name = ''
      this.transaction_name = ''
      this.amount = 0
      this.category_id = 0
      this.account_code = ''
    },

    resetErros: function() {
      this.errors.name = ''
      this.errors.transaction_name = ''
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
      if (!this.category_id) {
        this.errors.category_id = 'Please select'
        isError = true
      }
      return !isError
    },
  }
}
</script>

