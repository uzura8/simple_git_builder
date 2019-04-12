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
import site from './site'
Vue.mixin({
  methods: {
    siteUri: site.uri,
    siteConfig: site.config,
    isEmpty: util.isEmpty,
    inArray: util.inArray,
  }
});

import moment from 'moment'
import 'moment/locale/ja'
moment.locale('ja');
Vue.filter('dateFormat', function (date, format='LLL') {
  return moment(date).format(format);
});

Vue.filter('numFormat', function (num) {
  return String(num).replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
});
Vue.filter('substr', function (text, num) {
  return util.substr(text, num, '...')
});

import flatPickr from 'vue-flatpickr-component'
Vue.component('flatPickr', flatPickr)
import TransactionRow from './components/TransactionRow'
Vue.component('TransactionRow', TransactionRow)
import TransactionEditModal from './components/TransactionEditModal'
Vue.component('TransactionEditModal', TransactionEditModal)
import TransactionActiveCheckbox from './components/TransactionActiveCheckbox'
Vue.component('TransactionActiveCheckbox', TransactionActiveCheckbox)
import InputCategory from './components/InputCategory'
Vue.component('InputCategory', InputCategory)
import UpdateCategory from './components/UpdateCategory'
Vue.component('UpdateCategory', UpdateCategory)
import InputDate from './components/InputDate'
Vue.component('InputDate', InputDate)

export {
  Vue,
  VueRouter,
  moment,
}
