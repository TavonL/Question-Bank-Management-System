import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Login from '@/components/Login';
import QuestionBank from '@/components/QuestionBank'

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            name: 'HelloWorld',
            component: HelloWorld
        },
        {
            path: '/login',
            component: Login,
            name: 'Login'
        },
        {
            path: '/2',
            component: QuestionBank,
            name: 'QuestionBank'
        },
        {
            path: '/3',
            component: QuestionBank,
            name: 'QuestionBank'
        },
        {
            path: '/4',
            component: QuestionBank,
            name: 'QuestionBank'
        },
        {
            path: '/5',
            component: QuestionBank,
            name: 'QuestionBank'
        },
        {
            path: '/6',
            component: QuestionBank,
            name: 'QuestionBank'
        },
        {
            path: '/7',
            component: QuestionBank,
            name: 'QuestionBank'
        },
    ]
});
