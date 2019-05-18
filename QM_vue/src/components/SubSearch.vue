<template>
<div>
<el-row>
  <el-col :span="24"><div><p></p></div></el-col>
</el-row>
<el-row>
  <el-col :span="2"><div><p></p></div></el-col>
  <el-col :span="20"><div>
  <el-card shadow="never">
    <el-form ref="conditionForm" :model="conditionForm" label-width="80px" size="mini">
    <el-form-item label="关键字">
      <el-input v-model="conditionForm.keyword" class="input-with-select">
        <el-select v-model="conditionForm.paper_grade" slot="append">
          <el-option label="初中试题" value="0"></el-option>
          <el-option label="高中试题" value="1"></el-option>
          <el-option label="大学试题" value="2"></el-option>
        </el-select>
      </el-input>
    </el-form-item>
    <el-form-item label="学科">
      <el-col :span="1">
      <el-select v-model="conditionForm.paper_subject" placeholder="请选择" class="el-select">
      <el-option
        v-for="item in optionsSubject"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
      </el-select>
    </el-col>
    </el-form-item>
    <el-form-item label="知识点" style="text-align:left">
      <el-cascader
        v-model="conditionForm.question_point"
        placehoder="请选择"
        :options="options"
        filterable
        :show-all-levels="false"
        change-on-select
      ></el-cascader>
    </el-radio-group>
    </el-form-item>
    <el-form-item label="题型" style="text-align:left">
      <el-radio-group v-model="conditionForm.question_type">
        <el-radio-button label="填空题" name="1"></el-radio-button>
        <el-radio-button label="单选题" name="2"></el-radio-button>
        <el-radio-button label="多选题" name="3"></el-radio-button>
        <el-radio-button label="应用题" name="4"></el-radio-button>
        <el-radio-button label="综合题" name="5"></el-radio-button>
        <el-radio-button label="不限" name="6"></el-radio-button>
    </el-radio-group>
    </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="submitForm('conditionForm')">搜索</el-button>
    <el-button @click="resetForm('conditionForm')">重置</el-button>
    </el-form-item>
    </el-form>
  </el-card> 
  </div></el-col>
  <el-col :span="2"><div><p></p></div></el-col>
</el-row>
  <!-- <p>test</p> -->

</div>
</template>

<script>
  export default {
    name: 'SubSearch',
    data() {
      return {
        conditionForm: {
          keyword: '',
          question_type: '不限',
          paper_subject:'',
          paper_grade: '0',
          knowledge_point: [],
        },
        optionsSubject: [{
          value: '1',
          label: '数学'
        }, {
          value: '2',
          label: '语文'
        }, {
          value: '3',
          label: '英语'
        }, {
          value: '4',
          label: '化学'
        }, {
          value: '5',
          label: '物理'
        },{
          value: '6',
          label: '不限'
        }],
        options: [{
            value: '0',
            label: '应该',
            children: [{
              value: '0',
              label: '自动'
              }]
            },{
            value:'1',
            label: '产生',
            value:'2',
            label: '不限',
          }],
    };
  },
    methods: {
      submitForm(formName) {
        console.log(this.conditionForm);
        this.$refs[formName].validate((valid) => {
          if (valid) {
            alert('submit!');
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        alert('reset!')
        this.$refs[formName].resetFields();
      }
    }
  };
</script>

<style>
  .input-with-select .el-input-group__append {
    background-color: #fff;
  }
  .input {
    width: 80%;
  }
  .el-select .el-input{
    width: 120px;
  }
</style>