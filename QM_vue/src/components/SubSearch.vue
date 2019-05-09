<template>
<div>
<el-row>
  <el-col :span="24"><div><p></p></div></el-col>
</el-row>
<el-row>
  <el-col :span="2"><div><p></p></div></el-col>
  <el-col :span="20"><div>
  <el-card shadow="never">
    <el-form ref="searchForm" :model="sizeForm" label-width="80px" size="mini">
    <el-form-item label="关键字">
      <el-input v-model="sizeForm.name" class="input-with-select">
        <el-select v-model="sizeForm.grade" slot="append">
          <el-option label="初中试题" value="0"></el-option>
          <el-option label="高中试题" value="1"></el-option>
          <el-option label="大学试题" value="2"></el-option>
        </el-select>
      </el-input>
    </el-form-item>
    <el-form-item label="学科">
      <el-col :span="1">
      <el-select v-model="value" placeholder="请选择" >
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
        v-model="sizeForm.point"
        placehoder="请选择"
        :options="options"
        filterable
        :show-all-levels="false"
        change-on-select
      ></el-cascader>
    </el-checkbox-group>
    </el-form-item>
    <el-form-item label="题型" style="text-align:left">
      <el-checkbox-group v-model="sizeForm.type">
        <el-checkbox-button label="也应该" name="type"></el-checkbox-button>
        <el-checkbox-button label="自动" name="type"></el-checkbox-button>
        <el-checkbox-button label="更新" name="type"></el-checkbox-button>
    </el-checkbox-group>
    </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="submitForm('searchForm')">搜索</el-button>
    <el-button @click="resetForm('searchForm')">重置</el-button>
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
        sizeForm: {
          name: '',
          region: '',
          date1: '',
          date2: '',
          delivery: false,
          type: [],
          resource: '',
          desc: '',
          grade: '2'
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
        value: '6',
        options: [{
            value: '0',
            label: '应该',
            children: [{
              value: '1',
              label: '自动'
              }]
            },{
            value:'2',
            label: '产生'
          }],
    };
  },
    methods: {
      submitForm(formName) {
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
</style>