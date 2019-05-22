<template>
<div>
  <mavon-editor ref="md1" class="inner-block mavon-editor"
  :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
  v-model="question.question_content"
  placeholder="缺少题干"
  :editable="false"/>
<el-collapse v-model="activeNames">
  <el-collapse-item title="查看答案" name="1">
    <mavon-editor ref="md2" class="inner-block mavon-editor"
    :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
    v-model="question.question_answer"
    placeholder="缺少答案"
    :editable="false"/>
  </el-collapse-item>
  <el-collapse-item title="查看解析" name="2">
    <mavon-editor ref="md3" class="inner-block mavon-editor"
    :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
    v-model="question.question_analy"
    placeholder="缺少解析"
    :editable="false"/>
  </el-collapse-item>
</el-collapse>
</div>
</template>

<script>
export default {
  name: 'QuestionDetail.vue',
  props: ['questionNo'],
  data () {
    return {
      question: {
        question_content: '测试一下',
        question_answer: '....',
        question_analy: '....',
      },
      activeNames:[],
      dialogVisible: false,
    }
  },
  watch: {
    questionNo: {
      immediate: true,
      handler(content) {
        // 请求题目内容
      }
    }
  },
  mounted (){
    this.$nextTick(() => {
      this.$refs.md1.$refs.vShowContent.style.background="#ffffff";
      this.$refs.md1.$refs.vShowContent.style.lineHeight="200%";
      this.$refs.md1.$refs.vShowContent.parentElement.parentElement.style.border="0px";
      this.$refs.md2.$refs.vShowContent.style.background="#ffffff";
      this.$refs.md2.$refs.vShowContent.style.lineHeight="200%";
      this.$refs.md2.$refs.vShowContent.parentElement.parentElement.style.border="0px";
      this.$refs.md3.$refs.vShowContent.style.background="#ffffff";
      this.$refs.md3.$refs.vShowContent.style.lineHeight="200%";
      this.$refs.md3.$refs.vShowContent.parentElement.parentElement.style.border="0px";
      // this.downloadAsPdf();
    });
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
