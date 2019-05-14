<template>
  <div>
  <el-card shadow="never" class="frame">
    <el-steps :active="curStep">
    <el-step title="步骤 1" description="基本信息"></el-step>
    <el-step title="步骤 2" description="编辑题目"></el-step>
    <el-step title="步骤 3" description="预览试卷"></el-step>
    <el-step title="步骤 4" description="上传试卷"></el-step>
    </el-steps>
  </el-card>
  <el-dialog title="编辑/预览" :visible.sync="editorVisible" >
  <Editor v-if="editorType=='C'" :content="curDomain.question_content" @new="updateContent"></Editor>
  <Editor v-if="editorType=='A'" :content="curDomain.question_analy" @new="updateContent"></Editor>
  </el-dialog>
  <el-card class="frame" shadow="never" v-if="curStep==1">
    <el-form :model="paperBasicForm" ref="paperBasicForm" label-width="100px" class="form" >
    <el-form-item
      prop="paper_source"
      label="试卷来源"
      :rules="{
        required: true, message: '必须选择试卷所属的市/区/学校', trigger: 'blur'
      }"
    >
    <el-cascader
      v-model="paperBasicForm.paper_source"
      class="cascader"
      placeholder="请选择试卷所属的市/区/学校"
      :options="sourceOptions"
      filterable
      :show-all-levels="false"
      change-on-select
    ></el-cascader>
    </el-form-item>
    <el-form-item
      prop="paper_year"
      label="试卷年份"
      :rules="{
        required: true, message: '必须选择试卷的年份', trigger: 'blur'
      }"
    >
    <el-date-picker
      value-format="yyyy"
      v-model="paperBasicForm.paper_year"
      type="year"
      placeholder="选择年">
    </el-date-picker>

    </el-form-item>
    <el-form-item
      prop="paper_grade"
      label="试卷年级"

      :rules="{
        required: true, message: '必须选择试卷对应的年级', trigger: 'blur'
      }"
    >
    <el-cascader
      v-model="paperBasicForm.paper_grade"
      placeholder="请选择试卷对应的年级"
      :options="gradeOptions"
      filterable
      :show-all-levels="false"
    ></el-cascader>
    </el-form-item>
    <el-form-item
      prop="paper_subject"
      label="试卷学科"
      :rules="{
        required: true, message: '必须选择试卷的学科', trigger: 'blur'
      }"
    >
      <el-cascader 
      ref="cascaderSubject"
      v-model="paperBasicForm.paper_subject" 
      :disabled="subjectDisabled" 
      :placeholder="subjectHint"
      :options="subjectOptions" 
      ></el-cascader>
    </el-form-item>
    <el-form-item
      prop="paper_suffix"
      label="试卷名"
    >
    <el-input class="input" placeholder="可选填，如期末/统考" v-model="paperBasicForm.paper_suffix">
      <template slot="prepend"> {{paper_prefix}} </template>
      <template slot="append"> 卷</template>
    </el-input>
    </el-form-item>
    <el-form-item>
    </el-form-item>

    <el-form-item>
      <el-button type="primary" @click="nextStep">下一步</el-button>
    </el-form-item>
  </el-form>
  </el-card>
  <el-card class="frame" shadow="never" v-if="curStep==2">
    <el-form :model="paperForm" ref="paperForm" label-width="100px" class="form" >
      <el-form-item
      v-for="(domain, index) in paperForm.domains"
      :label="'第' + (index+1) + '题'"
      :key="domain.key"
      :prop="'domains.' + index + '.value'"
    > 
      <el-row>
      <el-col :span="16">
        <el-cascader size="medium"
          class="cascader"
          v-model="domain.question_point"
          placeholder="请选择该题知识点"
          :options="pointOptions"
          filterable
          :show-all-levels="false"
          change-on-select
        ></el-cascader>
        <el-select class="select" v-model="domain.question_type" placeholder="请选择该题题型" size="medium">
          <el-option
            v-for="item in typeOptions"
            :key="item.value"
            :label="item.label"
            :value="item.value">
          </el-option>
        </el-select>
        <br>
        <el-input 
          class="textarea"
          type="textarea"
          :autosize="{ minRows: 4, maxRows: 15}"
          placeholder="请输入题干"
          v-model="domain.question_content">
        </el-input>
        <br>
        <el-button size="small" type="primary" @click.prevent="openEditor(domain,'C')">编辑/预览题干</el-button>
        <AnswerEditor :type="domain.question_type" @newAnswer="updateAnswer($event, domain)"></AnswerEditor>
        <el-input 
          class="textarea"
          type="textarea"
          :autosize="{ minRows: 4, maxRows: 15}"
          placeholder="请输入解析"
          v-model="domain.question_analy">
        </el-input>
        <br>
        <el-button size="small" type="primary" @click.prevent="openEditor(domain, 'A')">编辑/预览解析</el-button>
        <br>
        <el-popover
          placement="top"
          width="160"
          v-model="domain.confirmVisible">
          <p>确定删除该题吗？</p>
          <div style="text-align: right; margin: 0">
            <el-button size="mini" type="text" @click.prevent="removeDomain(domain)">确定</el-button>
            <el-button type="primary" size="mini" @click="domain.confirmVisible = false">取消</el-button>
          </div>
        <el-button slot="reference" size="small">删除该题</el-button>
        </el-popover>
      </el-col>
<!--       <el-col :span="8" >
        <el-upload
          class="avatar-uploader"
          action="https://jsonplaceholder.typicode.com/posts/"
          :show-file-list="false"
          :on-success="handleAvatarSuccess"
          :before-upload="beforeAvatarUpload">
          <img v-if="imageUrl" :src="imageUrl" class="avatar">
          <i v-else class="el-icon-plus avatar-uploader-icon"></i>
        </el-upload>
      </el-col> -->
    </el-row>
    </el-form-item>
    <el-form-item>
      <el-button type="default" @click="addDomain">新增题</el-button>
      <!-- <el-button type="default" @click="addQuestion">新增小题</el-button> -->
    </el-form-item>
    <el-form-item>
      <el-button type="default" @click="prevStep">上一步</el-button>
      <el-button type="primary" @click="nextStep">下一步</el-button>
    </el-form-item>
    </el-form>
  </el-card>
  <el-card class="frame" shadow="never" v-if="curStep==3">
    <span>预览部件</span>
    <el-button type="default" @click="prevStep">上一步</el-button>
    <el-button type="primary" @click="nextStep">下一步</el-button> 
  </el-card>
  <el-card class="frame" shadow="never" v-if="curStep==4">
    <span>上传下载部分</span>
    <el-button type="default" @click="prevStep">上一步</el-button>
    <el-button type="primary">提交</el-button>
  </el-card>
  </div>
</template>
<script>
  import Editor from '@/components/Editor';
  import AnswerEditor from '@/components/AnswerEditor';
  export default {
    components:{Editor, AnswerEditor},
    data() {
      return {
        paperForm: {
          domains: [{
            question_content: '',
            question_type: '',
            question_point: [],
            question_answer: '',
            question_analy: '',
            confirmVisible: '',
          }],
        },
        paperBasicForm: {
          paper_subject: [],
          paper_grade: [],
          paper_source:[],
          paper_year:'',

        },
        sourceOptions:[{
          value: 1,
          label: '上海市',
          children:[{
            value: 2,
            label: '宝山区',
            children:[{
              value: 3,
              label: '上海大学'
            }]
          }]
        }],
        gradeOptions:[{
          value: 1,
          label: '初中',
          children:[{
            value: 2,
            label: '初中一年级',
            },{
            value:3,
            label: '初中二年级' 
            }
          ]
        },{
          value: 4,
          label: '大学',
          children:[{
            value: 5,
            label: '大学三年级'
          }]
        }],
        subjectOptions:[{
          value:1,
          label:'数学'
        }],
        curStep: 1,
        subjectDisabled:false,
        subjectHint:"请先选择试卷对应的年份",
        sourceMap: {
          3: "上海大学"
        },
        gradeMap: {
          2: "初中一年级",
          3: "初中二年级",
          5: "大学三年级"
        },
        subjectMap: {
          1: "数学"
        },
        pointOptions: [{
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
        typeOptions:[{
          value: 1,
          label:'填空题'
        },{
          value: 2,
          label:'单选题'
        },{
          value:3, 
          label: '多选题'
        },{
          value: 4,
          label:'应用题'
        },{
          value: 5,
          label:'综合题'
        }],
        imageUrl: '',
        editorVisible: false,
        editorType: '',
        curDomain: {},
        curContent:'',
    }
  },
    computed:{
      paper_prefix: function(){
        let source = this.paperBasicForm.paper_source;
        let grade = this.paperBasicForm.paper_grade;
        let subject = this.paperBasicForm.paper_subject;
        let res = '';
        if (source.length > 0)
          res += this.sourceMap[source[source.length-1]];
        if (this.paperBasicForm.paper_year != '')
          res += this.paperBasicForm.paper_year + '年';
        if (grade.length > 0)
          res += this.gradeMap[grade[grade.length-1]];
        if (subject.length > 0)
          res += this.subjectMap[subject[subject.length-1]];
        return res;
      }
    },
    methods: {
      submitForm(formName) {
        console.log(this.paperBasicForm.paper_source)
        console.log(this.$refs['cascaderSource'].currentLabels)
        console.log(this.$refs['cascaderGrade'].currentLabels)
        console.log(this.$refs['cascaderSubject'].currentLabels)
      },
      nextStep() {
        if(this.curStep < 4)
          this.curStep += 1;
      },
      prevStep() {
        if(this.curStep > 1)
          this.curStep -= 1;
      },
      removeDomain(item) {
        item.confirmVisible = false;
        let index = this.paperForm.domains.indexOf(item);
        if (index !== -1) {
          this.paperForm.domains.splice(index, 1)
        }
      },
      addDomain() {
        this.paperForm.domains.push({
          key: Date.now(),
          question_content: '',
          question_type: '',
          question_point: [],
          question_answer: '',
          question_analy: '',
          confirmVisible: '',
          child: [],
        });
      },
      handleAvatarSuccess(res, file) {
        this.imageUrl = URL.createObjectURL(file.raw);
      },
      beforeAvatarUpload(file) {
        const isJPG = file.type === 'image/jpeg';
        const isLt2M = file.size / 1024 / 1024 < 2;

        if (!isJPG) {
          this.$message.error('上传头像图片只能是 JPG 格式!');
        }
        if (!isLt2M) {
          this.$message.error('上传头像图片大小不能超过 2MB!');
        }
        return isJPG && isLt2M;
      },
      openEditor(domain, type){
        this.curDomain = domain;
        this.editorVisible = true;
        this.editorType = type;
      },
      updateContent(newContent){
        console.log(this.editorType, newContent);
        if (this.editorType == 'C'){
          this.curDomain.question_content = newContent;
        }
        else if (this.editorType == 'A'){
          this.curDomain.question_analy = newContent;
        }
      },
      updateAnswer($event, domain){
        domain.question_answer = $event;
        console.log('newAnswer', domain.question_answer);
      }

  }
}

</script>
<style scoped>
.frame{
  margin-top:2%;
  width:80%;
  margin-left:auto;
  margin-right:auto;
}
/*.step{
  width:80%;
}*/
.form{
  margin-top: 2%;
  margin-left:auto;
  margin-right:auto;
}
.button{
  text-align: center;
}
.input {
  width: 55%;
} 
.cascader{
  width: 55%;
}
.textarea{
  margin-top: 1%;
  margin-bottom: 1%;
  width: 95%;
}
.title{
  margin-left: 1%;
  margin-right: 0.5%;
}
.el-select .el-input__inner {
  width: 360px;
}
.avatar-uploader .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}
.avatar-uploader .el-upload:hover {
  border-color: #409EFF;
}
.avatar-uploader-icon {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>