import Vue from 'vue';
import VueRouter from 'vue-router';
import Food from '@/components/Food.vue';
import Worker from '@/components/Worker.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/food',
    name: 'Food',
    component: Food,
  },
  {
    path: '/worker',
    name: 'Worker',
    component: Worker,
  },

];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes,
});

export default router;
