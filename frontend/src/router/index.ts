import { createRouter, createWebHistory } from 'vue-router'

const Login = () => import('../views/Login.vue')
const Register = () => import('../views/Register.vue')
const Reset = () => import('../views/Reset.vue')
const Home = () => import('../views/Home.vue')
const Records = () => import('../views/Records.vue')
const Me = () => import('../views/Me.vue')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/register', component: Register },
    { path: '/reset', component: Reset },
    { path: '/home', component: Home },
    { path: '/records', component: Records },
    { path: '/me', component: Me }
  ]
})

export default router