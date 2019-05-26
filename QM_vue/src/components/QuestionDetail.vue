<template>
<div>
  <div>
<!--     <mavon-editor ref="md1" class="inner-block mavon-editor"
    :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
    v-model="question.question_content"
    placeholder="缺少题干"
    :editable="false"/> -->
    <!-- <div class="block" v-html="question.question_content"></div> -->
  <el-collapse v-model="activeNames">
    <el-collapse-item title="题目信息" name="0">
      <div class="info-block">
      <el-tag class="tag">题目来源</el-tag> {{question.paper_name}}
      </div>
      <div class="info-block">
      <el-tag class="tag">知识点</el-tag><span  v-for="text, index in question.knowledge_point" :key="index">{{text}}</span>
      </div>
      <div class="info-block">
      <el-tag class="tag">难度</el-tag>
      <el-rate
        class="rate"
        v-model="question.question_diff"
        disabled
        :max="3"
        show-score
        text-color="#ff9900"
        :score-template="rateText[question.question_diff-1]">
      </el-rate>
      </div>
    </el-collapse-item>
    <el-collapse-item title="题目" name="1">
      <div class="block" v-html="question.question_content"></div>
    </el-collapse-item>
    <el-collapse-item title="查看答案" name="2">
<!--       <mavon-editor ref="md2" class="inner-block mavon-editor"
      :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
      v-model="question.question_answer"
      placeholder="缺少答案"
      :editable="false"/> -->
      <div class="block" v-html="question.question_answer"></div>
    </el-collapse-item>

    <el-collapse-item title="查看解析" name="3">
<!--       <mavon-editor ref="md3" class="inner-block mavon-editor"
      :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
      v-model="question.question_analy"
      placeholder="缺少解析"
      :editable="false"/> -->
      <div class="block" v-html="question.question_analy"></div>
    </el-collapse-item>
  </el-collapse>
  </div>
</div>

</template>

<script>
export default {
  name: 'QuestionDetail.vue',
  props: ['questionNo'],
  data () {
    return {
      rateText:['简单','中等','难'],
      question: {
        question_content: '测试一下',
        question_answer: '....',
        question_analy: '....',
      },
      activeNames:['1'],
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
      dialogVisible: false,
    }
  },
  computed: {
  },
  watch: {
    questionNo: {
      immediate: true,
      handler(questionNo) {
        this.activeNames = ['1']
        this.$axios({
          method:'get',
          url:'/api/get/QuestionDetail?question_no=' + questionNo,
        }).then((response) =>{          //这里使用了ES6的语法
          console.log('detail', response.data)
          if(response.data.question_type == 5){
            this.question.question_content = response.data.question_content+ '<br>';
            for(let i=0; i<response.data.little_question.length; i++){
              let index = '<el-tag>('+(i+1)+')</el-tag>'
              this.question.question_content += index + response.data.little_question[i].question_content +'<br>';
              this.question.question_answer += index + response.data.little_question[i].question_answer + '<br>';
            }
            this.question.question_analy = response.data.question_analy;
            this.question.knowledge_point = response.data.knowledge_point;
            this.question.question_diff = response.data.question_diff;
            this.question.paper_name = response.data.paper_name;
          }
          else{
            this.question = response.data;
          }
          console.log('detail', this.question);
        }).catch((error) =>{
            //console.log(error);      //请求失败返回的数据
        });
      }
    }
  },
  created (){
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
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.info-block{
  margin-bottom: 5px;
}
.tag{
  margin-right: 10px;
  margin-bottom: 5px;
}
span{
  margin-right: 5px;
}
.rate{
  margin-top: 10px;
  margin-left: 5px;
}
</style>
