<template>
  <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="align">
  <el-form-item label="用户名" class="align username">
    <el-input 
    v-model="ruleForm.userName" 
    :disabled="true">
    </el-input>
  </el-form-item>
  <el-form-item
    v-if='pwdButtonSeen'
  >
  <el-button @click="changePwd">修改密码</el-button>
  </el-form-item>
  <div v-if='pwdChangeSeen' class="align password">
  <el-form-item 
    label="新密码"
    prop="pass"
  >
  <el-input 
    type='password'
    v-model="ruleForm.pass"
    autocomplete="off" >
    </el-input>
  </el-form-item>
  <el-form-item 
    label="确认新密码"
    prop="checkPass"
  >
    <el-input 
    type='password'
    v-model="ruleForm.checkPass"
    autocomplete="off">
    </el-input>
  </el-form-item>
  <el-form-item class="align">
    <el-button type="primary" @click="submitForm('ruleForm')">提交</el-button>
    <el-button type="default" @click="cancelForm('ruleForm')">取消</el-button>
  </el-form-item>
  </div>
</el-form>
</template>
<script>
 export default {
    data() {
        var validatePass = (rule,value,callback)=>{
            if(value === ''){
                callback(new Error('密码不能为空'))
            }else{
               if (this.ruleForm.checkPass !== '') {
                    this.$refs.ruleForm.validateField('checkPass');
                }
                callback(); 
            }
        };
        var validatePass2 = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入新密码'));
        } else if (value !== this.ruleForm.pass) {
          callback(new Error('两次输入密码不一致!'));
        } else {
          callback();
        }
      };
        return {
           ruleForm: {
          pass: '',
          checkPass: '',
          userName: 'admin',
        },
          pwdChangeSeen: false,
          pwdButtonSeen: true,
        rules: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          checkPass: [
            { validator: validatePass2, trigger: 'blur' }
          ],
        }
        };
    },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('修改密码成功，请重新登陆！');
            this.pwdChangeSeen=false;
            this.pwdButtonSeen=true;
            /*准备数据库修改操作，
            1.传递数据到数据库
            2.修改用户表
            */
            /*完成数据库修改操作*/
            this.ruleForm.pass='';
            this.ruleForm.checkPass='';
            this.$router.push({ path: '/login'});
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      changePwd() {
        this.pwdChangeSeen=true;
        this.pwdButtonSeen=false;
      },
      cancelForm(formName){
        this.pwdChangeSeen=false;
        this.pwdButtonSeen=true;
      }
    }
  }
</script>
<style scoped>
.username{
    margin-top:5%;
    width:30%;
}
.password{
    width:30%;
}
.align{
  margin-left:auto;
  margin-right:auto;
  text-align: center;
}
</style>