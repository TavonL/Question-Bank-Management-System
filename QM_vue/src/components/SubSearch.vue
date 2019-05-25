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
          <el-option label="小学试题" :value="1"></el-option>
          <el-option label="初中试题" :value="2"></el-option>
          <el-option label="高中试题" :value="3"></el-option>
        </el-select>
      </el-input>
    </el-form-item>
    <el-form-item label="知识点" style="text-align:left">
      <el-cascader
        v-model="conditionForm.knowledge_point"
        placehoder="请选择"
        :options="knowOpts"
        filterable
        :show-all-levels="false"
        change-on-select
      ></el-cascader>
    </el-radio-group>
    </el-form-item>
    <el-form-item label="学科">
      <el-col :span="1">
      <el-select v-model="conditionForm.paper_subject" placeholder="请选择" class="el-select">
      <el-option
        v-for="item in subjectOpts"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
      </el-select>
    </el-col>
    </el-form-item>

    <el-form-item label="题型" style="text-align:left">
      <el-radio-group v-model="conditionForm.question_type">
        <el-radio-button v-for="item, index in typeOpts" :key="index" :label="item.value">{{item.label}}</el-radio-button>
    </el-radio-group>
    </el-form-item>
    <el-form-item label="难度" style="text-align:left">
      <el-radio-group v-model="conditionForm.question_diff">
        <el-radio-button v-for="item, index in diffOpts" :key="index" :label="item.value">{{item.label}}</el-radio-button>
    </el-radio-group>
    </el-form-item>
    <el-form-item label="来源" style="text-align:left">
    <el-cascader
      v-model="conditionForm.paper_source"
      class="cascader"
      placeholder="请选择试卷所属的市/区/学校"
      :options="sourceOpts"
      filterable
      :show-all-levels="false"
      change-on-select
    ></el-cascader>
    </el-form-item>
    <el-form-item label="性质" style="text-align:left">
      <el-radio-group v-model="conditionForm.paper_nature">
        <el-radio-button v-for="item, index in propertyOpts" :key="index" :label="item.value">{{item.label}}</el-radio-button>
    </el-radio-group>
  </el-form-item>
    <el-form-item>
    <el-button type="primary" @click="submitForm('conditionForm')">搜索</el-button>
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
          question_diff:0,
          question_type: 0,
          paper_subject: 0,
          paper_grade: 0,
          knowledge_point: [0],
          paper_nature: 0,
          paper_source: [0]
        },
        subjectOpts: this.DICTS.subjectOpts,
        sourceOpts: [{
          value:0,
          no:0,
          label: '不限',
        }],
        knowOpts: [{
          value:0,
          no:0,
          label: '不限',
        }],
        diffOpts: this.DICTS.diffOpts,
        propertyOpts: this.DICTS.propertyOpts,
        typeOpts: this.DICTS.typeOpts,
    };
  },
    methods: {
      submitForm(formName) {
        console.log(this.sourceOpts);
        console.log(this.knowOpts);
        let conditions = {
          keyword: this.conditionForm.keyword,
          question_diff: this.conditionForm.question_diff,
          question_type: this.conditionForm.question_type,
          paper_subject: this.conditionForm.paper_subject,
          paper_source: this.getSourceNo(),
          paper_grade: this.DICTS.gradeOpts[this.conditionForm.paper_grade].no,
          knowledge_point: this.getKnowPtNo(),
          paper_nature: this.conditionForm.paper_nature,
        }
        this.$emit('newcondition',conditions);
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      getKnowPtNo(){
        let temp = this.knowOpts[this.conditionForm.knowledge_point[0]];
        for(let i=1; i < this.conditionForm.knowledge_point.length; i++){
          temp = temp.children[this.conditionForm.knowledge_point[i]-1];
        }
        return temp.no;
      },
      getSourceNo(){
        let temp = this.sourceOpts[this.conditionForm.paper_source[0]];
        for (let i=1; i < this.conditionForm.paper_source.length; i++){
          temp = temp.children[this.conditionForm.paper_source[i]-1];
        }
        return temp.no;
      }
    },

  created(){
    this.$axios({
        method:'get',
        url:'/api/get/KnowledgePoints'
      }).then((response) => {
        console.log(response);
        this.knowOpts.push.apply(response.data);
      }).catch((error) => {
        //console.log(error);
      });
    this.$axios({
        method:'get',
        url:'/api/get/SourcesNo'
      }).then((response) => {
        console.log(response);
        this.sourceOpts.push.apply(response.data);
      }).catch((error) => {
      });
  },
  watch: {
    '$route':{
      immediate: true,
      handler (to, from) {
        this.conditionForm.paper_grade = this.$route.params.grade - '0';
        //console.log(this.conditionForm.paper_grade);
        this.submitForm();
      }
    }
  }
}

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