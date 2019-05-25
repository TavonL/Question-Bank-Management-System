<template>
  <div>
  <MainIndex activeIndex="3"></MainIndex>
  <div  ref="step">
  <el-card shadow="never" class="frame">
    <el-steps :active="curStep">
    <el-step title="步骤 1" description="基本信息"></el-step>
    <el-step title="步骤 2" description="编辑题目"></el-step>
    <el-step title="步骤 3" description="预览上传"></el-step>
    </el-steps>
  </el-card>
  </div>
  <el-dialog title="编辑/预览" :visible.sync="editorVisible" @close="curQuestion.question_content+=' ';curQuestion.question_content+= ' '">
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
      }">
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
      }">
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
      label="默认卷名"
    >
    <el-input class="input" placeholder="可选填，如期末/统考" v-model="paperInfoForm.paper_suffix">
      <template slot="prepend"> {{paper_prefix}} </template>
      <template slot="append"> 卷</template>
    </el-input>
    </el-form-item>
    <el-form-item
      prop="paper_freename"
      label="自定义卷名"
    >
    <el-input class="input" placeholder="如有需要可自定义卷名" v-model="paperInfoForm.paper_freename">
      <template slot="append">卷</template>
    </el-input>
    </el-form-item>
  </el-form>
  <div class="next">
    <el-button type="primary" @click="nextStep">下一步</el-button>
  </div>
    
  </el-card>
  <el-card class="frame" shadow="never" v-if="curStep==2">
    <el-row>
    <el-col :span="18">
    <el-form :model="questionsForm" ref="questionsForm" label-width="130px" class="form" >
      <el-form-item :id="'q' + index"
      v-for="(question, index) in questionsForm.questions"
      :key="index"> 
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
      <el-row :span="24">
      <el-col :span="20">
        <div >
          <span>题目难度</span>
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
          v-model="question.knowledge_point"
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
    </el-col>
    <el-col :span="4" class="time-line-block">
      <transition class="fade" name="el-fade-in-linear">
      <div class="block" ref="timeline" v-if="timelineShow">
        <!-- <el-timeline> -->
          <el-dropdown  @command="goAnchor">
            <el-button type="primary">
              题目导航<i class="el-icon-arrow-down el-icon--right"></i>
            </el-button>
            <el-dropdown-menu slot="dropdown">
              <el-dropdown-item :command="'#q'+index" v-for="question, index in questionsForm.questions":key="index">{{'第'+(index+1)+'题'}}</el-dropdown-item>
            </el-dropdown-menu>
          </el-dropdown>
<!--           <el-timeline-item ref="timeline-item" :type="BtnType[Number(index==curItem)]" placement="top" v-for="question, index in questionsForm.questions"
          :key="index"> {{'第'+(index+1)+'题'}}
          <el-button size="mini" type="default" @click.prevent="goAnchor('#q'+index,index)" circle 
          icon="el-icon-d-arrow-right" class="icon-button"></el-button> -->
          <!-- </el-timeline-item> -->
        <!-- </el-timeline> -->
      </div>
    </transition>
    </el-col>
  </el-row>
    <el-alert class="alert" v-if="questionsCheckedInfoVisible"
      :title="questionsCheckedInfo"
      type="error">
    </el-alert>
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
        BtnType : ['default','primary'],
        curItem: 0,
        questionsForm: {
          questions: [{
            question_diff: '',
            question_content: '',
            question_type: '',
            knowledge_point: [],
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
          paper_freename: "",
        },
        sourceOptions:[{
          value: 1,
          label: '上海市',
          no: 3,
          children:[{
            value: 1,
            label: '宝山区',
            no: 2,
            children:[{
              value: 1,
              label: '上海大学',
              no:1
            }]
          }]
        }],
        gradeOptions:this.DICTS.gradeOpts.slice(1),
        subjectOptions:this.DICTS.subjectOpts.slice(1),
        curStep: 1,
        subjectDisabled:false,
        subjectHint:"请先选择试卷对应的年份",

        pointOptions: [{
            value: 1,
            label: '解析几何',
            no: 1,
            children: [{
              value: 1,
              label: '椭圆',
              no:2
              }]
            },{
            value:1,
            label: '排列组合',
            no: 3,
          }],
        typeOptions:this.DICTS.typeOpts.slice(1),
        imageUrl: '',
        editorVisible: false,
        editorType: '',
        curQuestion: {},
        curContent:'',
        rate: {
          colors: ['#1abc9c','#f39c12','#e74c3c'],
          texts: ['简单', '中等', '难']
        },
        questionsCheckedInfoVisible: false,
        questionsCheckedInfo: '',
        timelineShow: 0,
    }
  },
    computed:{
      paper_prefix: function(){
        let source = this.paperInfoForm.paper_source;
        let grade = this.paperInfoForm.paper_grade;
        let subject = this.paperInfoForm.paper_subject;
        let res = '';
        if (source.length > 0){

          let temp = this.sourceOptions[this.paperInfoForm.paper_source[0]-1];
          //console.log(temp);
          for (let i=1; i < this.paperInfoForm.paper_source.length; i++){
            //console.log(temp);
            temp = temp.children[this.paperInfoForm.paper_source[i]-1];
          }
          res += temp.label;
        }
        if (this.paperInfoForm.paper_year != '')
          res += this.paperInfoForm.paper_year + '年';
        if (grade.length > 0){
          res += this.gradeOptions[grade[0]-1].children[grade[1]-1].label;
        }
        if (subject.length > 0)
          res += this.subjectOptions[subject[0]-1].label;
        this.paperInfoForm.paper_prefix = res;
        //console.log(res);
        return res;

      }
    },
    methods: {
      validateForm(formName) {
        let res = false;
        this.$refs[formName].validate((valid) => {
          if (valid) {
            //console.log("ok")
            res = true;
          } else {
            //console.log('error submit!!');
            res = false;
          }
        });
        //console.log(res);
        return res;
      },
      getSourceNo(form, opts){
        let temp = opts[form.paper_source[0]-1];
        //console.log(temp);
        for (let i=1; i < form.paper_source.length-1; i++){
          temp = temp.children[form.paper_source[i]-1];
        }
        return temp.no;
      },
      getKnowPtsNo(form, opts){
        let temp = opts[form.knowledge_point[0]-1];
        for (let i=1; i < form.knowledge_point.length-1; i++){
          temp = temp.children[form.knowledge_point[i]-1];
        }
        return temp.no;
      },
      getPaperName(){
        if(this.paperInfoForm.paper_freename == '')
          return this.paperInfoForm.paper_prefix + (this.paperInfoForm.paper_suffix||'');
        return this.paperInfoForm.paper_freename;
      },
      uploadPaper() {
        let paperInfoForm = {
          paper_subject: this.paperInfoForm.paper_subject[0],
          paper_grade: this.DICTS.gradeOpts[this.paperInfoForm.paper_grade[0]].children[this.paperInfoForm.paper_grade[1]].no,
          paper_source: this.getSourceNo(this.paperInfoForm, this.sourceOptions),
          paper_year:this.paperInfoForm.paper_year,
          paper_name: this.getPaperName() + '卷',
        };

        let questionsForm = [];
        for (let i=0; i < this.questionsForm.questions.length; i++){
          questionsForm.push({
            question_diff: this.questionsForm.questions[i].question_diff,
            question_content: this.questionsForm.questions[i].question_content,
            question_type: this.questionsForm.questions[i].question_type,
            knowledge_point: this.getKnowPtsNo(this.questionsForm.questions[i], this.pointOptions),
            question_answer: this.questionsForm.questions[i].question_answer,
            question_analy: this.questionsForm.questions[i].question_analy,
          });
        }
        this.$axios({
            method:'post',
            url:'/uploadPaper',
            data:this.qs.stringify({    //这里是发送给后台的数据
                paperInfoForm:this.paperInfoForm,
                questionsForm:this.questions,
            })
        }).then((response) =>{          //这里使用了ES6的语法
            //console.log(response);       //请求成功返回的数据
            this.$router.push({name:'QuestionBank'});
            sessionStorage.removeItem('uploadQuestions');
            sessionStorage.removeItem('uploadPaperInfo');
        }).catch((error) =>{
            //console.log(error);      //请求失败返回的数据
        });
      },
      checkQuestions(questions, mode=1){
        for(let i=0; i < questions.length; i++){
          //console.log(questions[i]);
          if (mode && questions[i].question_diff == ''){
            this.questionsCheckedInfo = "请输入第"+ (i+1) + "题的难度";
            this.questionsCheckedInfoVisible = true;
            return false;
          }
          else if(mode && questions[i].knowledge_point.length == 0){
            this.questionsCheckedInfo = "请输入第"+ (i+1) + "题的知识点";
            this.questionsCheckedInfoVisible = true;
            return false;
          }
          else if(questions[i].question_content == ''){
            this.questionsCheckedInfo = "请输入第"+ (i+1) + "题的题干";
            this.questionsCheckedInfoVisible = true;
            return false;
          }
          else if(questions[i].question_type != 5 && questions[i].question_answer == ''){
            this.questionsCheckedInfo = "请输入第"+ (i+1) + "题的答案";
            this.questionsCheckedInfoVisible = true;
            return false;
          }
          else if(mode && questions[i].question_type == 5){
            let res = this.checkQuestions(questions[i].question_answer, 0);
            if(!res){
              this.questionsCheckedInfo = "请输入第"+ (i+1) + "题的答案";
              this.questionsCheckedInfoVisible = true;
              return false;
            }
          }
          else if(mode && questions[i].question_analy == ''){
            this.questionsCheckedInfo = "请输入第"+ (i+1) + "题的分析";
            this.questionsCheckedInfoVisible = true;
            return false;
          }
        }
        return true;
      },
      nextStep() {
        //console.log(this.curStep);
        if(this.curStep >= 3)
          return;
        if(this.curStep === 1 && this.validateForm('paperInfoForm')){
          this.curStep += 1;
        }
        else if (this.curStep == 2 && this.checkQuestions(this.questionsForm.questions)){
          //console.log('curStep 2 ok');
          this.curStep += 1;
          this.questionsCheckedInfoVisible = false;
        }
        else if(this.curStep == 3){
          //console.log("else");
          this.curStep += 1;
        }
        this.$nextTick(() => {
          if(this.curStep == 2){
            this.offsetTop =this.$refs.step.offsetTop;
            window.addEventListener('scroll', this.handleScroll, true); 
          }
        });
        if(this.curStep != 2){
          this.timelineShow = 0;
          window.removeEventListener('scroll', this.handleScroll,true);
        }
        sessionStorage.setItem('uploadQuestions', JSON.stringify(this.questionsForm));
        sessionStorage.setItem('uploadPaperInfo', JSON.stringify(this.paperInfoForm));
      },
      prevStep() {
        if(this.curStep <= 1)
          return;
        this.curStep -= 1;
        this.$nextTick(() => {
          if(this.curStep == 2){
            this.offsetTop =this.$refs.step.offsetTop;
            console.log(this.$refs.step.offsetTop);
            window.addEventListener('scroll', this.handleScroll, true); 
          }
        });
        if(this.curStep != 2){
          this.timelineShow = 0;
          window.removeEventListener('scroll', this.handleScroll,true);
        }
      },
      removeQuestion(item) {
        item.confirmVisible = false;
        let index = this.questionsForm.questions.indexOf(item);
        if (index !== -1) {
          this.questionsForm.questions.splice(index, 1);
        }
      },
      addQuestion() {
        this.questionsForm.questions.push({
          question_diff: 0,
          question_content: '',
          question_type: '',
          knowledge_point: [],
          question_answer: '',
          question_analy: '',
          confirmVisible: false,
          figures_url: '',

        });
      },
      openEditor(question, type){
        this.curQuestion = question;
        this.editorVisible = true;
        this.editorType = type;
      },
      updateContent(newContent, figures_url){
        if (this.editorType == 'C'){
          this.curQuestion.question_content = newContent;
        }
        else if (this.editorType == 'A'){
          this.curQuestion.question_analy = newContent;
        }
        this.editorVisible = false;
      },
      updateAnswer($event, question){
        question.question_answer = $event;
        //console.log(question);
        // //console.log('newAnswer', question.question_answer);
        this.editorVisible = false;
      },
      toPaperPreview(){
        let routeData = this.$router.resolve({
          name: "PaperPreview",
        });
        window.open(routeData.href, '_blank');
      },
      //锚点跳转
      goAnchor(selector) {
        // this.curItem = index;
        this.$el.querySelector(selector).scrollIntoView();
      },
      handleScroll: function () {
        let _pos = this.$refs.step.getBoundingClientRect().top;
        console.log('top', _pos);
        if(_pos < -30){
          console.log("show!")
          this.timelineShow = 1;
        }
        else{
          console.log("hide")
          this.timelineShow = 0;
        }
        for(let i=0; i < this.questionsForm.questions.length; i++){
          if (_pos == this.$el.querySelector('#q'+i).getBoundingClientRect().top){
            this.curItem = i;
          }
        }
      }
  },
  created(){
    this.$axios({
      method:'get',
      url:'/getKnowldgePoints'
    }).then((response) => {
      //console.log(response);
    }).catch((error) => {
      //console.log(error);
    });
  },
  mounted(){
    // sessionStorage.clear();
    //console.log(sessionStorage.getItem("uploadPaperInfo"));
    if(sessionStorage.getItem("uploadPaperInfo") != null){
      
      this.paperInfoForm = JSON.parse(sessionStorage.getItem("uploadPaperInfo"));
      //console.log(this.paperInfoForm);
    }
    if(sessionStorage.getItem("uploadQuestions") != null){
      this.questionsForm = JSON.parse(sessionStorage.getItem("uploadQuestions"));
    }
  },
  destroyed: function () {
    window.removeEventListener('scroll', this.handleScroll);   //  离开页面清除（移除）滚轮滚动事件
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
  margin-top: 0%;
}
.alert {
  width: 30%;
  text-align: center;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 1%;
  margin-top: 1%;
}
.time-line-block{
  margin-top: 5%;
  margin-bottom:10%;
  right: 200px;
  position: fixed;
  top: 10px;
  transition: all 0.8s;
}
.icon-button{
  margin-right: 2px;
  margin-left: 2px;
  
}
.fade-enter{
  opacity:0;
}
.fade-enter-active{
  transition:opacity .5s;
}
.fade-leave-active{
  transition:transform .5s;
}
.fade-leave-to{
  transform:translateX(10px);
}

</style>