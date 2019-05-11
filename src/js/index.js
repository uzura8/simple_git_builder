import '@babel/polyfill';

import {Vue, VueRouter} from './bootstrap';
import './common';

import store from './store'

import Top from './templates/top';
import About from './templates/about';
import Performance from './templates/performance';
import Transactions from './templates/transactions';
import TransactionPreset from './templates/TransactionPreset';
import BudgetsSetting from './templates/BudgetsSetting';
import CategorySetting from './templates/CategorySetting';
import NotFound from './templates/notfound';

const router = new VueRouter({
  mode: 'history',
  saveScrollPosition: true,
  routes: [
    { path: '/', component: Top },
    { path: '/about', component: About },
    { path: '/performance', name: 'Performance', component: Performance },
    { path: '/transactions', name: 'Transactions', component: Transactions },
    { path: '/setting/budgets', name: 'BudgetsSetting', component: BudgetsSetting },
    { path: '/setting/category', name: 'CategorySetting', component: CategorySetting },
    { path: '/setting/presets', name: 'TransactionPreset', component: TransactionPreset },
    { path: '/notfound', component: NotFound },
    { path: '*', redirect: '/notfound' }
  ],
  scrollBehavior (to, from, savedPosition) {
    if (to.hash) {
      return { selector: to.hash };
    } else if (savedPosition) {
      return savedPosition;
    } else {
      return { x: 0, y: 0 };
    }
  }
});

router.beforeEach((to, from, next) => {
  store.dispatch('setHeaderMenuOpen', false)
  next();
});

new Vue({
  el: '#app',
  data: {
  },
  computed: {
    isHeaderMenuOpen: function () {
      return store.state.common.isHeaderMenuOpen
    },
  },
  methods: {
    toggleHeaderMenuOpen: function () {
      store.dispatch('setHeaderMenuOpen', !this.isHeaderMenuOpen)
    },
  },
  store,
  router,
});
