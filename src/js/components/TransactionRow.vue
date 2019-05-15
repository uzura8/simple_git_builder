<template>
<tr :class="{ 'has-background-grey-lighter': transaction.is_disabled}">
  <td>
    <transaction-active-checkbox :transaction="transaction" class="u-mt3" />
  <td>
    <span class="is-hidden-mobile">{{transaction.date | dateFormat('MM/DD(ddd)')}}</span>
    <span class="is-hidden-tablet">{{transaction.date | dateFormat('DD(ddd)')}}</span>
  </td>
  <td>{{transaction.name}}</td>
  <td>{{transaction.amount | numFormat()}}</td>
  <td><update-category
        :categoryId="transaction.category_id"
        v-model="updateCategoryId"
        :isRight="true"
        :transactionId="transaction.id"
        :btnSize="'small'" /></td>
  <td>{{transaction.account_name | substr(12)}}</td>
  <td>
    <div class="dropdown is-right" :class="{'is-active':isDropdownActive}">
      <div class="dropdown-trigger">
        <button
          class="button is-small"
          aria-haspopup="true"
          aria-controls="dropdown-menu"
          @click="isDropdownActive = !isDropdownActive">
          <span>
            <b-icon pack="fas" size="is-small" icon="edit"></b-icon>
          </span>
          <span class="icon is-small">
            <i class="fas fa-angle-down" aria-hidden="true"></i>
          </span>
        </button>
      </div>
      <div class="dropdown-menu" id="dropdown-menu" role="menu">
        <div class="dropdown-content">
          <a class="dropdown-item" @click="isModalActive = true">
            <b-icon pack="fas" size="is-small" icon="pencil-alt"></b-icon>
            <span>Edit</span>
          </a>
        </div>
      </div>
    </div>

    <transaction-edit-modal
      :isModalActive="isModalActive"
      v-on:close-modal="isModalActive = false"
      :transactionId="transaction.id"
      :updateCategoryId="updateCategoryId"
      :dispButtonLabel="false"
      :buttonSize="'is-small'" />
  </td>
</tr>
</template>

<script>
export default {
  props: {
    transaction: {
      type: Object,
      default: {},
    },
  },

  data () {
    return {
      isDropdownActive: false,
      isModalActive: false,
      updateCategoryId: 0,
    }
  },

  computed: {
  },

  watch: {
    isModalActive (val) {
      if (val === false) this.isDropdownActive = false
    },
  },

  created() {
    this.updateCategoryId = this.transaction.category_id
  },

  methods: {
  },
}
</script>
