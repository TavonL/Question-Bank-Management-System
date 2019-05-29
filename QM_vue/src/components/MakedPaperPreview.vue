<template>
  <div>
  <el-button @click.prevent="downloadDocx1">下载试卷(word)</el-button>
  <el-button @click.prevent="downloadDocx2">下载答案(word)</el-button>
  <div v-html="questionsContent" class="page download"></div>
  <div v-html="questionsAnswer" class="page download_answer"></div>
<!--   <div id="paperHTML" class="page">
    <mavon-editor ref="md" class="inner-block mavon-editor"
    :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
    v-html="questionsContent"
    placeholder="缺少题干"
    :editable="false"/>
  <div class="block" v-for="question, index in questions" :key="index">
  </div>
</div> -->
</div>
</template>
<script>

import saveAs from "file-saver";
import "../../static/jquery.wordexport";
import Dicts from '@/global/Dicts';
export default {

  name: 'MakedPaperPreview',
  data () {
    return {
      questions: [],
      questionsContent: '',
      paperName: '',
      questionsAnswer:'',
    };
  },
  methods: {
    getQuestionPoint(question_point_array){
      // //console.log(question_point_array);
      let res = [];
      if(question_point_array.length < 1){
        return;
      }
      res.push(this.pointOptions[question_point_array[0]]);
      for (let i=1; i < question_point_array.length; i++){
        res.push(res[i-1].children[question_point_array[i]]);
      }
      return res;
    },
    downloadDocx1(){
      $('.download').wordExport(this.paperName);
      // $('<div>' + this.questionsContent + '</div>').wordExport("test");
    },
    downloadDocx2(){
      $('.download_answer').wordExport(this.paperName + '答案');
      // $('<div>' + this.questionsContent + '</div>').wordExport("test");
    },
    showBlankRes(question_answer){
      //console.log(question_answer);
      let res = "";
      for(let i=0; i < question_answer.length; i++){
        res += question_answer[i].value + ' ';
      }
      //console.log(res);
      return res;
    },
  },
  mounted (){
    this.questions = JSON.parse(sessionStorage.getItem("MakedPaperQuestions"));
    console.log(this.questions);
    let paperInfo = JSON.parse(sessionStorage.getItem("MakedPaperInfo"));
    let suffix = ['填空题<br>','单选题<br>','多选题<br>','应用题<br>','综合题<br>'];
    let prefix = ['一','二','三','四','五'];
    let curType = 0, k = 0;
    this.paperName = paperInfo.paperTitle;

    this.questionsAnswer = '<h3 style="text-align:center">' +  this.paperName + '</h3>';
    this.questionsContent += '<h3 style="text-align:center">' +  this.paperName + '</h3>';
    this.questionsContent += '<h4 style="text-align:center"> 总分' +  paperInfo.totalScore + '分 </h4>';
    this.questionsContent += '<h4 style="text-align:center"> 学号&nbsp;___________&nbsp;姓名&nbsp;___________&nbsp;成绩&nbsp;___________ </h4><br>';
    for (let i=0; i < this.questions.length; i++){

      if(k < 5 && curType != this.questions[i].question_type){
        curType = this.questions[i].question_type;
        this.questionsContent += '<p><span>' + prefix[k] +'、 '+ suffix[curType-1] + "(每小题"+this.questions[i].points+'分)'+'</span></p>';
        this.questionsAnswer += '<p><span>' + prefix[k] +'、 '+ suffix[curType-1] + '</span></p>';
        k += 1;
      }
      if(this.questions[i].question_type < 4){
        let answer = this.questions[i].question_answer;
        if(this.questions[i].question_type == 3){
          answer = answer[0].join(" ") + ' ' + answer[1];
        }
        else if(this.questions[i].question_type == 1){
          answer = ''
          for(let j=0; j < this.questions[i].question_answer.length; j++){
            answer += this.questions[i].question_answer[j].value + ' ';
          }
        }
        this.questionsAnswer += (i+1) + '. ' + answer + '; ';
      }
      if(this.questions[i].question_content.slice(0,3) == '<p>'){
        this.questionsContent += '<p>' + (i+1) + '. '+ this.questions[i].question_content.slice(3);
      }
      else{
        this.questionsContent += '<p>' + (i+1) + '. </p>'+ this.questions[i].question_content;
      }
      if (this.questions[i].question_type == 4){
          if(this.questions[i].question_answer.slice(0,3) == '<p>'){
            this.questionsAnswer += '<p>' + (i+1) + '. ' + this.questions[i].question_answer.slice(3);
          }
          else{
            this.questionsAnswer += '<p>' + (i+1) + '. </p>' + this.questions[i].question_answer;
          }
         this.questionsContent += "<br><br><br><br><br><br><br>";
      }
      if (this.questions[i].question_type == 5){
        for (let j=0; j < this.questions[i].question_answer.length; j++){
          //console.log(this.questions[i].question_answer[j]);
          if(this.questions[i].question_answer[j].question_answer.slice(0,3) == '<p>'){
            this.questionsAnswer += '<p>('+ (j+1) +') ' + this.questions[i].question_answer[j].question_answer.slice(3);
          }
          else{
            this.questionsAnswer += '<p>('+ (j+1) +') </p>' + this.questions[i].question_answer[j].question_answer.slice(3);
          }
          
          if(this.questions[i].question_answer[j].question_content.slice(0,3) == '<p>'){
            this.questionsContent += '<p>('+ (j+1) +') ' + this.questions[i].question_answer[j].question_content.slice(3);
          }
          else{
            this.questionsContent += '<p>('+ (j+1) +') </p>' + this.questions[i].question_answer[j].question_content.slice(3);
          }
          if(this.questions[i].question_answer[j].question_type == 4){
            this.questionsContent += '<br><br><br><br><br><br>';
          }
        }
      }
    }
    // this.md2word();
    // console.log(this.questionsContent);
    console.log(this.questionsAnswer);

    this.$nextTick(() => {
      //console.log(this.$refs);
      //console.log(this.$refs.md.$refs.vShowContent.parentElement.parentElement);
      // this.$refs.md.$refs.vShowContent.style.background="#ffffff";
      // this.$refs.md.$refs.vShowContent.style.lineHeight="200%";
      // this.$refs.md.$refs.vShowContent.parentElement.parentElement.style.border="0px";
      try{
          $('img').style.height = "auto";
          $('img').style.width = "auto";
          $('img').style.maxWidth = "100%";
          $('img').style.maxHeight = "100%";
      }
      catch(err){}
      for (let i=0; i < $('img').length; i++){
        $('img')[i].style.height = "auto";
        $('img')[i].style.width = "auto";
        $('img')[i].style.maxWidth = "100%";
        $('img')[i].style.maxHeight = "100%";
      }
    //   console.log('img', $('img'));
    //    $('img').attr('src', function () {
    //     if (/^https?:\/\//.test(this.src) && this.src.indexOf(location.hostname) == -1)//不同源将img改为本域下的代理页面负责下载图片变为同源
    //         return 'mydownloadpage.ashx?url=' + encodeURIComponent(this.src);
    //     return this.src;
    // })
    });
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
p{
  text-align: center;
}

body
{
    margin: 0;
    padding: 0;
    background-color: #FAFAFA;
    font: 12pt "Tahoma";
}
*
{
    box-sizing: border-box;
    -moz-box-sizing: border-box;
}
.page
{
    width: 21cm;
    min-height: 29.7cm;
    padding: 2cm;
    margin: 1cm auto;
    border: 1px #D3D3D3 solid;
    border-radius: 5px;
    background: white;
    box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
}
img{
 width:auto;
 height:auto;
 max-width:100%;
 max-height:100%;
}
.subpage
{
    padding: 1cm;
    border: 5px red solid;
    height: 256mm;
    outline: 2cm #FFEAEA solid;
}
@page
{
    size: A4;
    margin: 0;
}
@media print
{
    .page
    {
        margin: 50px;
        border: initial;
        border-radius: initial;
        width: initial;
        min-height: initial;
        box-shadow: initial;
        background: initial;
        page-break-after: always;
    }
}
</style>
