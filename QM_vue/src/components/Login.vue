/* eslint-disable */
<template>
  <el-form :model="loginForm" :rules="rules" ref="LoginForm" label-position="left" label-width="0px" class="demo-ruleForm login-container">
    <h3 class="title">试题库登录</h3>
    <el-form-item prop="username">
      <el-input type="text" v-model="loginForm.username" auto-complete="off" placeholder="账号"></el-input>
    </el-form-item>
    <el-form-item prop="password">
      <el-input type="password" v-model="loginForm.password" auto-complete="off" placeholder="密码"></el-input>
    </el-form-item>
    <el-checkbox style="margin: 0px 10px 15px auto" v-model="checkedPwd" checked class="remember">记住密码</el-checkbox>
    <el-checkbox style="margin: 0px auto 15px 10px" v-model="checkedLogin"  class="remember">3天内自动登录</el-checkbox>
    <el-form-item style="width:100%;">
      <el-button type="primary" style="width:100%;" @click="handleSubmit" :loading="logining">登录</el-button>
      <!--<el-button @click.native.prevent="handleReset2">重置</el-button>-->
    </el-form-item>
  </el-form>
</template>

<script>
export default {
  data () {
    return {
      logining: false,
      loginForm: {
        username: '',
        password: ''
      },
      rules: {
        username: [
          { required: true, message: '请输入账号', trigger: 'blur' }
        ],
        checkPass: [
          { required: true, message: '请输入密码', trigger: 'blue' }
        ]
      },
      checked: true
    }
  },
  methods: {
    // handleSubmit () {
    //   this.$refs.LoginForm.validate((valid) => {
    //     this.$axios({
    //       method:'post',
    //       url:'/login',
    //       data:this.qs.stringify({
    //         username: this.loginForm.username,
    //         password: Base64.encode(_this.loginForm.password),
    //       })
    //     }).then((response) =>{
    //         console.log(response); 


    //         localStorage.setItem('token', token);
    //         commit('auth_success', token, user)
    //         resolve(resp)
    //         axios.defaults.headers.common['Authorization'] = token
    //         this.$router.push({ path: '/' })
    //     }).catch((error) =>{
    //         console.log(error);
    //         commit('auth_error', err);
    //         reject(err);
    //     });
        
    //   })
    // }
  }
}
</script>

<style scoped>
  .login-container {
    /*box-shadow: 0 0px 8px 0 rgba(0, 0, 0, 0.06), 0 1px 0px 0 rgba(0, 0, 0, 0.02);*/
    -webkit-border-radius: 5px;
    border-radius: 5px;
    -moz-border-radius: 5px;
    background-clip: padding-box;
    margin: 180px auto;
    width: 350px;
    padding: 35px 35px 15px 35px;
    background: #fff;
    border: 1px solid #eaeaea;
    box-shadow: 0 0 25px #cac6c6;
    .title {
      margin: 0px auto 40px auto;
      text-align: center;
      color: #505458;
    }
    .remember {
      margin: 0px 0px 35px 0px;
    }
  }
</style>
