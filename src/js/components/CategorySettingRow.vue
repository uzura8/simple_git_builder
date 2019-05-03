<template>
<tr>
  <td>{{category.name}}</td>
  <td v-if="isEditable">
    <b-field grouped>
      <b-input
        placeholder="Please input sublabel"
        type="text"
        name="sublabel"
        ref="sublabel"
        expanded
        v-model="sublabel"
        @blur="blurInput"
        @focus="focus($event.target)"
        @keydown.enter.native="updateSublabel"
        @keyup.esc.native="cancel" />
      <p class="control">
        <button class="button is-info" @mousedown="updateSublabel">OK</button>
      </p>
    </b-field>
  </td>
  <td v-else @click="changeEditable">
    <span>{{sublabel}}</span>
    <b-icon icon="edit" pack="fas" size="is-small" class="is-pulled-right has-text-grey-lighter" />
  </td>
</tr>
</template>

<script>
export default {
  props: {
    category: {
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
      sublabel: '',
    }
  },

  computed: {
  },

  watch: {
  },

  created() {
    this.sublabel = this.category.sublabel
  },

  methods: {
    changeEditable() {
      this.tmp = this.sublabel
      this.isEditable = true
      this.$nextTick(() => this.$refs.sublabel.focus())
    },

    updateSublabel() {
      this.isUpdated = true
      if (this.sublabel == this.tmp) {
        this.resetEditable()
        return
      }
      const params = {
        categoryId: this.category.id,
        values: {
          sublabel: this.sublabel
        }
      }
      this.$store.dispatch('updateCategory', params)
        .catch(err => Promise.reject(err))
        .then(() => {
          this.resetEditable(false)
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
      this.resetEditable()
    },

    resetEditable(isRecoverSublabel = true) {
      if (isRecoverSublabel) this.sublabel = this.tmp
      this.isFocus = false
      this.isEditable = false
      this.isUpdated = false
    },
  },
}
</script>
