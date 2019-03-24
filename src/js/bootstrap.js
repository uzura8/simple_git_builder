import 'es6-promise/auto'

import Vue from 'vue';

import Vuex from 'vuex'
Vue.use(Vuex)

import VueRouter from 'vue-router';
Vue.use(VueRouter);

import Buefy from 'buefy';
Vue.use(Buefy);

import {site, util} from './shared';
Vue.mixin({
  methods: {
    siteUri: site.uri,
    siteConfig: site.config,
    isEmpty: util.isEmpty,
    inArray: util.inArray,
  }
});

import moment from 'moment';
import 'moment/locale/ja';
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


export {
  Vue,
  VueRouter,
  moment,
}
