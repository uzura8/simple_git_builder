import {Vue, VueRouter} from './bootstrap';
import './common';

import store from './store'

//import AriItem from './components/AriItem';
//Vue.component('AriItem', AriItem);

import Top from './templates/top';
import About from './templates/about';
import Transactions from './templates/transactions';
import NotFound from './templates/notfound';

const router = new VueRouter({
  mode: 'history',
  saveScrollPosition: true,
  routes: [
    { path: '/', component: Top },
    { path: '/about', component: About },
    { path: '/transactions', name: 'Transactions', component: Transactions },
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

new Vue({
  el: '#app',
  data: {
    isHeaderMenuOpen: false,
  },
  store,
  router,
});
