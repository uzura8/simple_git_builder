<template>
<tr>
  <td>
    <transaction-preset-edit-modal
      :presetId="preset.id"
      :dispButtonLabel="false"
      :buttonSize="'is-small'" />
  </td>
  <td>{{preset.name}}</td>
  <td>{{preset.transaction_name}}</td>
  <td>{{preset.amount | numFormat()}}</td>
  <td v-text="getCategoryName(preset.category_id)"></td>
  <td>
    <span v-if="preset.account_name">{{preset.account_name | substr(12)}}</span>
    <span v-else>-</span>
  </td>
  <td>
    <button class="button is-small" @click="confirmDelete">
      <b-icon icon="trash-alt" pack="fas" />
    </button>
  </td>
</tr>
</template>

<script>
export default {
  props: {
    preset: {
      type: Object,
      default: {},
    },
  },

  data () {
    return {
    }
  },

  computed: {
    category () {
      return this.$store.getters.category(this.preset.category_id)
    },
  },

  watch: {
  },

  created() {
  },

  methods: {
    getCategoryName: function() {
      if (this.isEmpty(this.category)) return ''
      return this.getCategoryLabel(this.category)
    },

    confirmDelete() {
      this.$dialog.confirm({
        title: 'Deleting preset',
        message: 'Are you sure you want to <b>delete</b> this preset? This action cannot be undone.',
        confirmText: 'Delete Preset',
        type: 'is-danger',
        hasIcon: true,
        onConfirm: () => {
          this.$toast.open('Deleted!')
        }
      })
    }
  },
}
</script>
