<template>
  <div>
  <MainIndex activeIndex="4"></MainIndex>
  <el-card shadow="never" class="frame">
    <el-steps :active="curStep">
    <el-step title="步骤 1" description="基本信息"></el-step>
    <el-step title="步骤 2" description="编辑题目"></el-step>
    <el-step title="步骤 3" description="预览上传"></el-step>
    </el-steps>
  </el-card>
  <el-dialog title="编辑/预览" :visible.sync="editorVisible" >
  <Editor v-if="editorType=='C'" :content="curQuestion.question_content" @new="updateContent"></Editor>
  <Editor v-if="editorType=='A'" :content="curQuestion.question_analy" @new="updateContent"></Editor>
  </el-dialog>
  <el-card class="frame" shadow="never" v-if="curStep==1">
    <el-form :model="paperInfoForm" ref="paperInfoForm" label-width="100px" class="form" >
    <el-form-item
      prop="paper_source"
      label="试卷来源"
      :rules="{
        required: true, message: '必须选择试卷所属的市/区/学校', trigger: 'blur'
      }"
    >
    <el-cascader
      v-model="paperInfoForm.paper_source"
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
      v-model="paperInfoForm.paper_year"
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
      v-model="paperInfoForm.paper_grade"
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
      v-model="paperInfoForm.paper_subject" 
      :disabled="subjectDisabled" 
      :placeholder="subjectHint"
      :options="subjectOptions" 
      ></el-cascader>
    </el-form-item>
    <el-form-item
      prop="paper_suffix"
      label="试卷名"
    >
    <el-input class="input" placeholder="可选填，如期末/统考" v-model="paperInfoForm.paper_suffix">
      <template slot="prepend"> {{paper_prefix}} </template>
      <template slot="append"> 卷</template>
    </el-input>
    </el-form-item>
    <el-form-item>
    </el-form-item>
  </el-form>
  <div class="next">
    <el-button type="primary" @click="nextStep">下一步</el-button>
  </div>
    
  </el-card>
  <el-card class="frame" shadow="never" v-if="curStep==2">
    <el-form :model="questionsForm" ref="questionsForm" label-width="130px" class="form" >
      <el-form-item
      v-for="(question, index) in questionsForm.questions"
      :key="question.key"
      :prop="'questions.' + index + '.value'"
    > 
      <template slot="label"> 
        第 {{index+1}} 题 
        <el-popover
          placement="top"
          width="160"
          v-model="question.confirmVisible">
          <p>确定删除该题吗？</p>
          <div style="text-align: right; margin: 0">
            <el-button size="mini" type="text" @click.prevent="removeQuestion(question)">确定</el-button>
            <el-button type="primary" size="mini" @click="question.confirmVisible = false">取消</el-button>
          </div>
          <!-- <el-button type="danger" icon="el-icon-delete" circle slot="reference" size="mini"></el-button> -->
          <el-button class="delete"  type="danger" slot="reference" size="mini">删除</el-button>
        </el-popover>
      </template>
      <el-row>
      <el-col :span="16">
        <div >
          <el-rate class="rate"
            v-model="question.question_diff"
            :colors="rate.colors"
            :high-threshold="3"
            :low-threshold="1"
            :max="3"
            show-text
            :texts="rate.texts"
            >
          </el-rate>
        </div>
        <el-cascader size="medium"
          class="cascader"
          v-model="question.question_point"
          placeholder="请选择该题知识点"
          :options="pointOptions"
          filterable
          change-on-select
        ></el-cascader>
        <el-select class="select" v-model="question.question_type" placeholder="请选择该题题型" size="medium">
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
          v-model="question.question_content">
        </el-input>
        <br>
        <el-button size="small" type="primary" @click.prevent="openEditor(question,'C')">编辑/预览题干</el-button>
        <AnswerEditor :type="question.question_type" :answer="question.question_answer" @newAnswer="updateAnswer($event, question)"></AnswerEditor>
        <el-input 
          class="textarea"
          type="textarea"
          :autosize="{ minRows: 4, maxRows: 15}"
          placeholder="请输入解析"
          v-model="question.question_analy">
        </el-input>
        <br>
        <el-button size="small" type="primary" @click.prevent="openEditor(question, 'A')">编辑/预览解析</el-button>
      </el-col>
    </el-row>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click.prevent="addQuestion">新增题目</el-button>
      <!-- <el-button type="default" @click="addQuestion">新增小题</el-button> -->
    </el-form-item>
    </el-form>
    <div class="next">
      <el-button type="default" @click.prevent="prevStep">上一步</el-button>
      <el-button type="primary" @click.prevent="nextStep">下一步</el-button>
    </div>
  </el-card>
  <el-card class="frame" shadow="never" v-if="curStep==3">
    <!-- <span>预览部件</span> -->
    <div class="block">
    <el-button type="primary" @click.prevent="toPaperPreview"> 试卷预览 </el-button>
    <el-button type="primary" @click.prevent="uploadPaper"> 上传试卷 </el-button>
    </div>
    <div class="next">
      <el-button type="default" @click.prevent="prevStep">上一步</el-button>
    </div>
  </el-card>
  </div>
</template>
<script>
  import MainIndex from '@/components/MainIndex';
  import Editor from '@/components/Editor';
  import AnswerEditor from '@/components/AnswerEditor';
  export default {
    components:{Editor, AnswerEditor, MainIndex},
    data() {
      return {
        questionsForm: {
          questions: [{
            question_diff: 0,
            question_content: '',
            question_type: '',
            question_point: [],
            question_answer: '',
            question_analy: '',
            confirmVisible: false,
          }],
        },
        paperInfoForm: {
          paper_subject: [],
          paper_grade: [],
          paper_source:[],
          paper_year:"",
          paper_prefix: "",
          paper_suffix: "",

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
          value: 0,
          label: '初中',
          children:[{
            value: 0,
            label: '初中一年级',
            },{
            value:1,
            label: '初中二年级' 
            }
          ]
        },{
          value: 1,
          label: '大学',
          children:[{
            value: 0,
            label: '大学三年级'
          }]
        }],
        subjectOptions:[{
          value:0,
          label:'数学'
        }],
        curStep: 1,
        subjectDisabled:false,
        subjectHint:"请先选择试卷对应的年份",
        sourceMap: {
          3: "上海大学"
        },
        pointOptions: [{
            value: '0',
            label: '解析几何',
            children: [{
              value: '0',
              label: '椭圆'
              }]
            },{
            value:'1',
            label: '排列组合'
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
        curQuestion: {},
        curContent:'',
        rate: {
          colors: ['#1abc9c','#f39c12','#e74c3c'],
          texts: ['简单', '中等', '难']
        }
    }
  },
    computed:{
      paper_prefix: function(){
        let source = this.paperInfoForm.paper_source;
        let grade = this.paperInfoForm.paper_grade;
        let subject = this.paperInfoForm.paper_subject;
        let res = '';
        if (source.length > 0)
          res += this.sourceMap[source[source.length-1]];
        if (this.paperInfoForm.paper_year != '')
          res += this.paperInfoForm.paper_year + '年';
        if (grade.length > 0){
          res += this.gradeOptions[grade[0]].children[grade[1]].label;
        }
        if (subject.length > 0)
          res += this.subjectOptions[subject[0]].label;
        this.paperInfoForm.paper_prefix = res;
        console.log(res);
        return res;

      }
    },
    methods: {

      uploadPaper() {
        console.log(this.questionsForm.questions);
        console.log(this.paperInfoForm.paper_source);
        this.$axios({
            method:'post',
            url:'/uploadPaper',
            data:this.qs.stringify({    //这里是发送给后台的数据
                paperInfoForm:this.paperInfoForm,
                questionsForm:this.questions,
            })
        }).then((response) =>{          //这里使用了ES6的语法
            console.log(response);       //请求成功返回的数据
            this.$router.push({name:'QuestionBank'});
            sessionStorage.removeItem('uploadQuestions');
            sessionStorage.removeItem('uploadPaperInfo');
        }).catch((error) =>{
            console.log(error);      //请求失败返回的数据
        });
      },
      nextStep() {
        if(this.curStep < 3)
          this.curStep += 1;
        sessionStorage.setItem('uploadQuestions', JSON.stringify(this.questionsForm));
        sessionStorage.setItem('uploadPaperInfo', JSON.stringify(this.paperInfoForm));
      },
      prevStep() {
        if(this.curStep > 1)
          this.curStep -= 1;
      },
      removeQuestion(item) {
        item.confirmVisible = false;
        let index = this.questionsForm.questions.indexOf(item);
        if (index !== -1) {
          this.questionsForm.questions.splice(index, 1)
        }
      },
      addQuestion() {
        this.questionsForm.questions.push({
          key: Date.now(),
          question_diff: 0,
          question_content: '',
          question_type: '',
          question_point: [],
          question_answer: '',
          question_analy: '',
          confirmVisible: false,
          child: [],
        });
      },
      openEditor(question, type){
        this.curQuestion = question;
        this.editorVisible = true;
        this.editorType = type;
      },
      updateContent(newContent){
        console.log(this.editorType, newContent);
        if (this.editorType == 'C'){
          this.curQuestion.question_content = newContent;
        }
        else if (this.editorType == 'A'){
          this.curQuestion.question_analy = newContent;
        }
      },
      updateAnswer($event, question){
        question.question_answer = $event;
        console.log(question);
        // console.log('newAnswer', question.question_answer);
      },
      toPaperPreview(){

        let routeData = this.$router.resolve({
          name: "PaperPreview",
        });
        window.open(routeData.href, '_blank');
      }
  },
  created(){
    this.$axios({
      method:'get',
      url:'/getKnowldgePoints'
    }).then((response) => {
      console.log(response);
    }).catch((error) => {
      console.log(error);
    });
  },
  mounted(){
    // sessionStorage.clear();
    console.log(sessionStorage.getItem("uploadPaperInfo"));
    if(sessionStorage.getItem("uploadPaperInfo") != null){
      
      this.paperInfoForm = JSON.parse(sessionStorage.getItem("uploadPaperInfo"));
      console.log(this.paperInfoForm);
    }
    if(sessionStorage.getItem("uploadQuestions") != null){
      this.questionsForm = JSON.parse(sessionStorage.getItem("uploadQuestions"));
    }
  }
}

</script>
<style scoped>
.frame{
  margin-top:2%;
  width:80%;
  padding-left: 20px;
  padding-right: 20px;
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
.delete{
  margin-left: 5%;
}
.next{
  text-align: center;
  margin-left: auto;
  margin-right: auto;
}
a{
  text-decoration:none;
  color: #000000;
}
.block {
  margin-top: 2%;
  margin-bottom: 2%;
}
.rate {
  margin-bottom: 1%;
  margin-top: 1%;
}
</style>