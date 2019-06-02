import 'es6-promise/auto'

import Vue from 'vue'

import Vuex from 'vuex'
Vue.use(Vuex)

import VueRouter from 'vue-router'
Vue.use(VueRouter);

import Buefy from 'buefy'
Vue.use(Buefy)

//import VeeValidate from 'vee-validate'
//Vue.use(VeeValidate)

import util from './util'
import listener from './listener'
import site from './site'
Vue.mixin({
  methods: {
    siteUri: site.uri,
    siteConfig: site.config,
    isEmpty: util.isEmpty,
    inArray: util.inArray,
    listen: listener.listen,
    destroyed: listener.destroyed,
    getCategoryLabel: function(category) {
      if (util.isEmpty(category)) return ''
      if (!util.isEmpty(category.sublabel)) return category.sublabel
      return category.name
    },
  },
});

import moment from 'moment'
import 'moment/locale/ja'
moment.locale('ja');
Vue.filter('dateFormat', function (date, format='LLL') {
  return moment(date).format(format);
});

Vue.filter('numFormat', function (num) {
  num = parseInt(num)
  if (isNaN(num)) return 0
  return String(num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
});
Vue.filter('substr', function (text, num) {
  return util.substr(text, num, '...')
});

import flatPickr from 'vue-flatpickr-component'
Vue.component('flatPickr', flatPickr)

import InputDate from './components/InputDate'
Vue.component('InputDate', InputDate)

import TransactionCategoryFilter from './components/TransactionCategoryFilter'
Vue.component('TransactionCategoryFilter', TransactionCategoryFilter)

import TransactionMonthNav from './components/TransactionMonthNav'
Vue.component('TransactionMonthNav', TransactionMonthNav)

import TransactionRow from './components/TransactionRow'
Vue.component('TransactionRow', TransactionRow)

import TransactionRowEditDropdown from './components/TransactionRowEditDropdown'
Vue.component('TransactionRowEditDropdown', TransactionRowEditDropdown)

import TransactionEditModal from './components/TransactionEditModal'
Vue.component('TransactionEditModal', TransactionEditModal)

import TransactionActiveCheckbox from './components/TransactionActiveCheckbox'
Vue.component('TransactionActiveCheckbox', TransactionActiveCheckbox)

import TransactionPresetRow from './components/TransactionPresetRow'
Vue.component('TransactionPresetRow', TransactionPresetRow)

import TransactionPresetEditModal from './components/TransactionPresetEditModal'
Vue.component('TransactionPresetEditModal', TransactionPresetEditModal)

import TransactionPresetDropdown from './components/TransactionPresetDropdown'
Vue.component('TransactionPresetDropdown', TransactionPresetDropdown)

import InputCategory from './components/InputCategory'
Vue.component('InputCategory', InputCategory)

import InputAccount from './components/InputAccount'
Vue.component('InputAccount', InputAccount)

import UpdateCategory from './components/UpdateCategory'
Vue.component('UpdateCategory', UpdateCategory)

import CategorySettingRow from './components/CategorySettingRow'
Vue.component('CategorySettingRow', CategorySettingRow)

import CategorySettingIsMonthlyCheckbox from './components/CategorySettingIsMonthlyCheckbox'
Vue.component('CategorySettingIsMonthlyCheckbox', CategorySettingIsMonthlyCheckbox)

import BudgetsSettingRow from './components/BudgetsSettingRow'
Vue.component('BudgetsSettingRow', BudgetsSettingRow)

export {
  Vue,
  VueRouter,
  moment,
}
