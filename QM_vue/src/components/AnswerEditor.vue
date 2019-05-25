<template>
<div class="block" v-if="curType == ''">
  答案：
  <el-input class="input" type="text" disabled placeholder="请先选择题型"/>
</div>

<div class="block" v-else-if="curType == 1">
  <!-- <el-input class="input" type="text" v-model="blankAnswers[0]" placeholder="请输入答案"/> -->
  <div class="block" v-for="(blank, index) in blankAnswers" :key="index">
    第 {{index + 1}} 空答案：
    <el-input v-model="blank.value" class="input" type="text" plackholder="请输入答案" @change="updateBlankAnswer">
    </el-input>
    <el-button type="danger" class="button" size="small" @click.prevent="delItem(blank, blankAnswers)" >删除该空</el-button>
  </div>

  <el-button class="button" type="primary" size="small" @click.prevent="newBlank">新增空</el-button>
</div>
<!-- 选择题 -->
<div class="block" v-else-if="curType == 2">
  答案：
    <el-radio-group v-model="radioAnswer1" size="mini" @change="updateRadioAnswer1">
      <el-radio-button label="A"></el-radio-button>
      <el-radio-button label="B"></el-radio-button>
      <el-radio-button label="C"></el-radio-button>
      <el-radio-button label="D"></el-radio-button>
    </el-radio-group>
  <br>
  其他(选填)：
  <el-input v-model="radioAnswer2" size="mini" type="text" class="input" @change="updateRadioAnswer2" ></el-input>
</div>

<div class="block" v-else-if="curType == 3">
  答案：
    <el-checkbox-group v-model="multiRadioAnswer1" size="mini" @change="updateMultiRadioAnswer">
      <el-checkbox-button label="A"></el-checkbox-button>
      <el-checkbox-button label="B"></el-checkbox-button>
      <el-checkbox-button label="C"></el-checkbox-button>
      <el-checkbox-button label="D"></el-checkbox-button>
      <el-checkbox-button label="E"></el-checkbox-button>
      <el-checkbox-button label="F"></el-checkbox-button>
    </el-checkbox-group>
  其他(选填，请用空格分割)：
  <el-input v-model="multiRadioAnswer2" size="mini" type="text" class="input" @change="updateMultiRadioAnswer" ></el-input>
</div>
<!-- 大题 -->
<div v-else-if="curType == 4">
  <el-dialog title="编辑/预览" :visible.sync="editorVisible" >
  <Editor :content="wordAnswer" @new="updateWordAnswer"></Editor>
  </el-dialog>
  <el-input 
    class="textarea"
    type="textarea"
    :autosize="{ minRows: 4, maxRows: 15}"
    placeholder="请使用编辑器编辑小题题干"
    v-model="wordAnswer"
    @change="updateWordAnswer">
  </el-input>
  <br>
  <el-button size="small" class="button" type="primary" @click.prevent="editorVisible=true">编辑/预览答案</el-button>
</div>

<div class="block" v-else-if="curType == 5">
<el-dialog title="编辑/预览" :visible.sync="subEditorVisible" @close="curQst.question_content+=''" >
<Editor :content="curQst.question_content" @new="updateSubQuestionContent"></Editor>
</el-dialog>
  <div class="block" v-for="(qst, index) in subQuestions" :key="index">
    第 {{index + 1}} 小问：
    <el-select v-model="qst.question_type" placeholder="请选择该小题题型" size="small" @change="updateCompreAnswer">
      <el-option
        v-for="item in typeOptions"
        :key="item.value"
        :label="item.label"
        :value="item.value">
      </el-option>
    </el-select>
    <el-button type="danger" class="button" size="small" @click.prevent="delItem(qst, subQuestions)" >删除该小题</el-button>
    <el-input 
    class="textarea"
    type="textarea"
    :autosize="{ minRows: 2, maxRows: 5}"
    placeholder="请使用编辑器编辑小题题干"
    v-model="qst.question_content"
    @change="updateCompreAnswer">
  </el-input>
  <br>
  <el-button size="small" class="button" type="primary" @click.prevent="openSubEditor(qst)">编辑/预览小题题干</el-button>
  <AnswerEditor :type="qst.question_type" :answer="qst.question_answer" @newAnswer="updateSubAnswer($event, qst)"></AnswerEditor>
  
  </div>
  <el-button class="button" type="primary" size="small" @click.prevent="newSubQuestion">新增小题</el-button>
</div>


</template>

<script>
import Editor from '@/components/Editor';
export default {
  name: 'AnswerEditor',
  props: ['type','answer'],
  components: {Editor},
  data () {
    return {
      curQst: [],
      subEditorVisible:false,
      editorVisible: false,
      wordAnswer: '',
      radioAnswer1: '',
      radioAnswer2: '',
      multiRadioAnswer1: [],
      multiRadioAnswer2: '',
      blankAnswers:[{
        key:'',
        value: ''
      }
      ],
      subQuestions:[],
      curType: this.type,
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
      }],
    }
  },
  computed:{
  },
  methods: {
    newBlank() {
      this.blankAnswers.push({
        key: '',
        value: '',
      });
    },
    newSubQuestion() {
      this.subQuestions.push({
        question_type: '',
        question_content: '',
        question_answer: '',
      });
    },
    delItem(item, items) {
      let index = items.indexOf(item);
      if (index !== -1) {
        items.splice(index, 1)
      }
    },
    openSubEditor(qst){
      this.curQst = qst;
      this.subEditorVisible = true;
    },
    updateBlankAnswer() {
      this.$emit('newAnswer', this.blankAnswers);
    },
    updateRadioAnswer1() {
      this.radioAnswer2 = '';
      this.$emit('newAnswer', this.radioAnswer1);
    },
    updateRadioAnswer2() {
      this.radioAnswer1 = '';
      this.$emit('newAnswer', this.radioAnswer2);
    },
    updateMultiRadioAnswer() {
      this.$emit('newAnswer', [this.multiRadioAnswer1, this.multiRadioAnswer2]);
    },
    updateWordAnswer(newAnswer){
      this.wordAnswer = newAnswer;
      this.editorVisible = false;
      this.$emit('newAnswer', this.wordAnswer);
    },
    updateCompreAnswer(newAnswer){
      console.log('compre?',console.log(newAnswer));
      this.$emit('newAnswer', this.subQuestions);
    },
    updateSubQuestionContent(newContent){
      this.subEditorVisible = false;
      this.curQst.question_content = newContent;
      console.log(this.subQuestions);
    },
    updateSubAnswer($event, question){
      question.question_answer = $event;
      this.$emit('newAnswer', this.subQuestions)
      console.log('newAnswer?',this.subQuestions);
    }
  },
  watch: {
    type: {
      immediate: true,
      handler(type) {
        // console.log(type);
        this.curType = type;
      }
    },
    answer: {
      immediate: true,
      handler(answer) {
        // console.log('curAnswer', answer);
        if (answer == ''){
          return;
        }
        if (this.curType == 1){
          this.blankAnswers = answer;
        }
        else if (this.curType == 2){
          if ('A' <= answer && answer <= 'D'){
            this.radioAnswer1 = answer;
          }
          else{
            this.radioAnswer2 = answer;
          }
        }
        else if (this.curType == 3){
          this.multiRadioAnswer1 = answer[0];
          this.multiRadioAnswer2 = answer[1];
        }
        else if (this.curType == 4){
          this.wordAnswer = answer;
        }
        else if (this.curType == 5){
          this.subQuestions = answer;
        }
      }
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.input {
  width: 50%;
}
.block {
  margin-top: 2%;
  margin-bottom: 1%;
}
.textarea{
  margin-top: 1%;
  margin-bottom: 1%;
  width: 95%;
}
</style>
