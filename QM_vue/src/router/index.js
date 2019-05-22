import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Login from '@/components/Login';
import QuestionBank from '@/components/QuestionBank';
import PersonalInfo from '@/components/PersonalInfo';
import QuestionUpload from '@/components/QuestionUpload';
import PaperPreview from '@/components/PaperPreview';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/login',
            component: Login,
            name: 'Login'
        },
        {
            path: '/QuestionBank/:grade',
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
            component: QuestionUpload,
            name: 'QuestionUpload'
        },
        {
            path: '/5',
            component: QuestionBank,
            name: 'QuestionBank'
        },
        {
            path: '/6',
            component: PersonalInfo,
            name: 'PersonalInfo'
        },
        {
            path: '/7',
            component: QuestionBank,
            name: 'QuestionBank'
        },
        {
            path: '/paperPreview',
            component: PaperPreview,
            name: 'PaperPreview',
        },
        {
            path:'*',
            redirect: '/QuestionBank/0'
        }
    ],
    // mode: 'history',
});
