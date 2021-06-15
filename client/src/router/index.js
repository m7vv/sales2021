import Vue from 'vue';
import VueRouter from 'vue-router';
import Food from '@/components/Food.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/food',
    name: 'Food',
    component: Food,
  },

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
