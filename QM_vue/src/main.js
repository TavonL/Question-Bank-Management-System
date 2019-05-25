// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue';
import App from './App';
import router from './router';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import 'font-awesome/css/font-awesome.min.css';

import axios from 'axios';
import qs from 'qs';
import mavonEditor from 'mavon-editor';
import 'mavon-editor/dist/css/index.css';
import '@/assets/iconfont.css';
import Vuex from 'vuex';
import VueUeditorWrap from 'vue-ueditor-wrap';
import '../static/UEditor/ueditor.config.js'
import '../static/UEditor/ueditor.all.js'
import '../static/UEditor/lang/zh-cn/zh-cn.js'

//引入公式插件。我们也是通过import的方式加进来的。
import '../static/UEditor/kityformula-plugin/addKityFormulaDialog.js'
import '../static/UEditor/kityformula-plugin/getKfContent.js'
import '../static/UEditor/kityformula-plugin/defaultFilterFix.js'
Vue.use(Vuex);
Vue.component('vue-ueditor-wrap', VueUeditorWrap);
Vue.use(mavonEditor);
Vue.use(ElementUI);
Vue.prototype.$axios = axios;
Vue.prototype.qs = qs;
Vue.config.productionTip = false;
// axios.defaults.baseURL = 'http://localhost:5000';


import Dicts from '@/global/dicts.vue';
Vue.prototype.DICTS = Dicts;
/* eslint-disable no-new */
new Vue({
    el: '#app',
    router,
    components: { App },
    template: '<App/>'
})
