<template>
<tr :class="{ 'has-background-grey-lighter': transaction.is_disabled}">
  <td>{{transaction.date | dateFormat('MM/DD(ddd)')}}</td>
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
    <div class="columns is-gapless u-mt0">
      <div class="column">
        <transaction-active-checkbox :transaction="transaction" class="u-mt3" />
      </div>
      <div class="column">
        <transaction-edit-modal
          :transactionId="transaction.id"
          :updateCategoryId="updateCategoryId"
          :dispButtonLabel="false"
          :buttonSize="'is-small'" />
      </div>
    </div>
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
      updateCategoryId: 0
    }
  },
  computed: {
  },
  watch: {
  },
  created() {
  },
  methods: {
  },
}
</script>
