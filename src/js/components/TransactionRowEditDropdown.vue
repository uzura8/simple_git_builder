
<template>
<div>
  <div class="dropdown is-right" :class="{'is-active':isActive}">
    <div class="dropdown-trigger">
      <button
        class="button is-small"
        aria-haspopup="true"
        aria-controls="dropdown-menu"
        @click="isActive = !isActive">
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
    @close-modal="isModalActive = false"
    :transactionId="transaction.id"
    :updateCategoryId="updateCategoryId"
    :dispButtonLabel="false"
    :buttonSize="'is-small'" />
</div>
</template>

<script>
export default {
  props: {
    transaction: {
      type: Object,
      default: {},
    },
    updateCategoryId: {
      type: Number,
      default: 0,
    },
  },
  data() {
    return {
      isActive: false,
      isModalActive: false,
    }
  },

  computed: {
  },

  watch: {
    isModalActive (val) {
      if (val === false) this.isActive = false
    },
  },

  created() {
    this.listen(window, 'click', function(e){
      if (!this.$el.contains(e.target)) {
        this.isActive = false
      }
    }.bind(this));
  },
  methods: {
  }
}
</script>
