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
  <td>
    <update-category
        :categoryId="transaction.category_id"
        v-model="updateCategoryId"
        :isRight="true"
        :transactionId="transaction.id"
        :btnSize="'small'" />
  </td>
  <td>{{transaction.account_name | substr(12)}}</td>
  <td>
    <Transaction-row-edit-dropdown
      :transaction="transaction"
      :updateCategoryId="updateCategoryId"/>
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
      updateCategoryId: 0,
    }
  },

  computed: {
  },

  watch: {
  },

  created() {
    this.updateCategoryId = this.transaction.category_id
  },

  methods: {
  },
}
</script>
