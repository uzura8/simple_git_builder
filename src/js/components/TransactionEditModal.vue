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
        <b-field label="Date">
          <input-date v-model="date" />
        </b-field>
        <b-field label="Content">
          <b-input
            type="text"
            placeholder="Please input content"
            required
            v-model="name">
          </b-input>
        </b-field>
        <b-field label="Amount">
          <b-input
            placeholder="Please input amount"
            type="number"
            required
            icon="yen-sign"
            icon-pack="fas"
            v-model="amount">
          </b-input>
        </b-field>
        <b-field label="Category">
          <input-category v-model="category_id" />
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
      values: {},
    }
  },
  computed: {
    transaction () {
      return this.$store.getters.transaction(this.transactionId)
    },
    isNew () {
      return this.isEmpty(this.transactionId)
    },
    date: {
      get () {
        if (!this.isEmpty(this.values.date)) return this.values.date
        return this.isNew ? '' : this.transaction.date
      },
      set (newValue) {
        this.values.date = newValue
      }
    },
    name: {
      get () {
        if (!this.isEmpty(this.values.name)) return this.values.name
        return this.isNew ? '' : this.transaction.name
      },
      set (newValue) {
        this.values.name = newValue
      }
    },
    amount: {
      get () {
        if (!this.isEmpty(this.values.amount)) return this.values.amount
        return this.isNew ? 0 : this.transaction.amount
      },
      set (newValue) {
        this.values.amount = newValue
      }
    },
    category_id: {
      get () {
        if (!this.isEmpty(this.values.category_id)) return this.values.category_id
        return this.isNew ? 0 : this.transaction.category_id
      },
      set (newValue) {
        this.values.category_id = newValue
      }
    },
  },
  created() {
  },
  methods: {
    save: function() {
      const updateKeys = Object.keys(this.values);
      if (this.isNew) {
      } else if (updateKeys) {
        const params = {
          transactionId: this.transaction.id,
          values: this.values,
        }
        this.$store.dispatch('updateTransaction', params)
          .catch(err => Promise.reject(err))
          .then(() => {
            this.isModalActive = false
          })
      }
    },
  }
}
</script>

