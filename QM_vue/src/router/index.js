import Vue from 'vue';
import Router from 'vue-router';
import HelloWorld from '@/components/HelloWorld';
import Login from '@/components/Login';
import QuestionBank from '@/components/QuestionBank';
import PersonalInfo from '@/components/PersonalInfo';
import QuestionUpload from '@/components/QuestionUpload';
import PaperPreview from '@/components/PaperPreview';
import QuestionCollector from '@/components/QuestionCollector';
Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/login',
            component: Login,
            name: 'Login'
        },
        {
            path: '/questionBank/:grade',
            component: QuestionBank,
            name: 'QuestionBank',
            meta: {
                title: "试题库",
                requireAuth: true
            }
        },
        {
            path: '/questionCollector',
            component: QuestionCollector,
            name: 'QuestionCollector',
            meta: {
                title: "我的收藏",
                requireAuth: true
            }
        },
        {
            path: '/questionUpload',
            component: QuestionUpload,
            name: 'QuestionUpload',
            meta: {
                title: "试题上传",
                requireAuth: true
            }
        },
        {
            path: '/5',
            component: QuestionBank,
            name: 'QuestionBank',
            meta: {
                title: "试题上传",
                requireAuth: true
            }
        },
        {
            path: '/6',
            component: PersonalInfo,
            name: 'PersonalInfo',
            meta: {
                title: "个人信息",
                requireAuth: true
            }
        },
        {
            path: '/7',
            component: QuestionBank,
            name: 'QuestionBank',
            meta: {
                title: "试题库",
                requireAuth: true
            }
        },
        {
            path: '/paperPreview',
            component: PaperPreview,
            name: 'PaperPreview',
            meta: {
                title: "试卷预览",
                requireAuth: true
            }
        },
        {
            path:'*',
            redirect: '/QuestionBank/1'
        }
    ]
});
// router.beforeEach((to, from, next) => {
//   if(to.matched.some(record => record.meta.requiresAuth)) {
//     if (store.getters.isLoggedIn) {
//       next()
//       return
//     }
//     next('/login')
//   } else {
//     next()
//   }
// });