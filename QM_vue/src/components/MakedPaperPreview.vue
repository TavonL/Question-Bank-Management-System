<template>
  <div>
  <el-button @click.prevent="downloadMD">下载MD测试</el-button>
  <el-switch
  v-model="answerVisible"
  active-text="显示答案">
</el-switch>
  <div id="paperHTML" class="page">
    <p>{{paperName}}</p>
    <mavon-editor ref="md" class="inner-block mavon-editor"
    :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
    v-model="questionsContent"
    placeholder="缺少题干"
    :editable="false"/>
  <div class="block" v-for="question, index in questions" :key="index">
  <div>
  </div>
    
    
  </div>
</div>
</div>
</template>
<script>
import marked from 'marked';

let rendererMD = new marked.Renderer();
marked.setOptions({
    renderer: rendererMD,
    gfm: true,
    tables: true,
    breaks: false,
    pedantic: false,
    sanitize: false,
    smartLists: true,
    smartypants: false
});

export default {
  name: 'MakedPaperPreview',
  data () {
    return {
      answerVisible:false,
      questions: [],
      questionsContent: '',
      paperName: '',
    };
  },
  methods: {
    getQuestionPoint(question_point_array){
      // console.log(question_point_array);
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
    downloadMD(){
      let aTag = document.createElement('a');
      let file_name = this.paperName + '.md';
      let blob = new Blob([this.questionsContent], {'endings':'native'});　　// 这个content是下载的文件内容，自己修改
      aTag.download = file_name;　　　　　　// 下载的文件名
      aTag.href = URL.createObjectURL(blob);
      aTag.click();　　　　　　　　　　　　　　
      URL.revokeObjectURL(blob);
    },
    showBlankRes(question_answer){
      console.log(question_answer);
      let res = "";
      for(let i=0; i < question_answer.length; i++){
        res += question_answer[i].value + ' ';
      }
      console.log(res);
      return res;
    },
    md2word(){
      this.$axios({
        method:'post',
        url:'/PaperPreview/md2word',
        data:this.qs.stringify({    //这里是发送给后台的数据
            paperName: this.paperName,
            questionsContent: this.questionsContent,
        })
      }).then((response) =>{          //这里使用了ES6的语法
        console.log(response)
      }).catch((error) =>{
          console.log(error);      //请求失败返回的数据
      });
    }
  },
  mounted (){

    this.questions = JSON.parse(sessionStorage.getItem("uploadQuestions")).questions;
    this.questions = this.questions.sort(function(a, b){return a.question_type - b.question_type});
    let paperInfo = JSON.parse(sessionStorage.getItem("uploadPaperInfo"));
    this.paperName = paperInfo.paper_prefix + (paperInfo.paper_suffix || '') + '卷';
    for (let i=0; i < this.questions.length; i++){
      this.questionsContent += (i+1) + ' . '+ this.questions[i].question_content + '\n\n';
      if (this.questions[i].question_type == 4){
         this.questionsContent += " \\\n \\\n \\\n \\\n \\\n \\\n \\\n";
      }
      if (this.questions[i].question_type == 5){
        for (let j=0; j < this.questions[i].question_answer.length; j++){
          console.log(this.questions[i].question_answer[j]);
          this.questionsContent += '('+ (j+1) +') ' + this.questions[i].question_answer[j].question_content + '\n\n';
          if(this.questions[i].question_answer[j].question_type == 4){
            this.questionsContent += ' \\\n \\\n \\\n \\\n \\\n';
          }
        }
      }
    }
    this.md2word();
    console.log(this.questionsContent);


    this.$nextTick(() => {
      console.log(this.$refs);
      console.log(this.$refs.md.$refs.vShowContent.parentElement.parentElement);
      this.$refs.md.$refs.vShowContent.style.background="#ffffff";
      this.$refs.md.$refs.vShowContent.style.lineHeight="200%";
      this.$refs.md.$refs.vShowContent.parentElement.parentElement.style.border="0px";
      // this.downloadAsPdf();
    });
  },
  computed: {
    addIndex(){
      return function(){
        return marked(content);
      };
    }
  }
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
