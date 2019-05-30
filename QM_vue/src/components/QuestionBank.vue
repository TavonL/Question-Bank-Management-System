<template>
  <div> 
    <MainIndex activeIndex="1"></MainIndex>
    <SubSearch @newcondition="updateCondition"></SubSearch @newcondition="updateCondition"> 
    <el-dialog
    title="查看详情"
    :visible.sync="questionDetailsVisible"
    width="80%">
      <QuestionDetail :questionNo="question_no"></QuestionDetail>
      <span slot="footer" class="dialog-footer">
        <el-button type="default" @click.prevent="questionDetailsVisible = false">关闭</el-button>
        <el-button type="primary" @click.prevent="nextQuestion">下一题</el-button>
      </span>
    </el-dialog>
    <div class="block pagination">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-size="100"
        layout="prev, pager, next, jumper"
        :total="totalPage">
      </el-pagination>
    </div>
    <el-row :gutter="10" v-for="o, i in row" :key="o" style="padding-top:20px">
    <el-col :span="2"><div><p></p></div></el-col>
    <el-col :span="10" v-for="(question, index) in curQuestions.slice((currentPage-1)*col*row+i*col,(currentPage-1)*col*row+(i+1)*col)" :key="index">
      <el-card class="box-card" shadow="hover" >
        <div class="item">
          <div style="height:300px; z-index:0">
          <div class="card" v-html="question.question_content"></div>
<!--           <mavon-editor ref="md" class="inner-block mavon-editor"
          :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
          v-model="question.question_content"
          placeholder="缺少题干"
          :editable="false"/> -->
          </div>
          <div class="card-footer over" >
            <time class="time">试题来源：{{question.paper_name}}</time>
            <el-button type="text" class="button" @click.prevent="readMore(question.question_no, index)">查看详情</el-button>
            <!-- <el-button type="text" class="button" @click.prevent="storeUp(question.question_no)">收藏</el-button> -->
          </div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="2"><div><p></p></div></el-col>
    </el-row>
    <div class="block pagination">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-size="100"
        layout="prev, pager, next, jumper"
        :total="totalPage">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import SubSearch from '@/components/SubSearch';
import MainIndex from '@/components/MainIndex';
import QuestionDetail from '@/components/QuestionDetail';
export default {
    name:'QuestionBank',
    components:{SubSearch, MainIndex, QuestionDetail},
    data(){
        return{
            conditionForm:{},
            question_no: 123,
            question_index: 0,
            questionDetailsVisible: false,
            row: 5,
            col: 2,
            pageSize: 10,
            curQuestions: [],
            currentPage:1,
            totalPage:1000,
        };
    },
    methods: {
      handleSizeChange(val) {
        //console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        if((this.currentPage-1) % 10 != 0)
          return;
        this.getQuestions(Math.floor((val-1)/10) * this.col * this.row, this.col*this.row*this.pageSize);
        //console.log(Math.floor((val-1)/10) * this.col * this.row);
        
      },
      readMore(question_no, index){
        this.question_no = question_no;
        this.questionDetailsVisible = true;
        this.question_index = index + 1;
      },
      nextQuestion(){
        if(this.curQuestions.length <= this.question_index){
          this.HintNoMore();
          return;
        }
        this.question_no = this.curQuestions[this.question_index].question_no;
        this.question_index += 1;
        if(this.question_index % (this.col * this.row) == 0){
          console.log(this.question_index);
          this.currentPage += 1;
          if((this.currentPage-1) % 10 == 0){
            this.question_index = 0;
            handleCurrentChange(this.currentPage);
          }
        }
      },
      HintNoMore() {
        const h = this.$createElement;
        this.$notify({
          title: '提示',
          message: h('i', '已经没有更多的题目了')
        });
      },
      storeUp(question_no){
        this.$axios({
            method:'get',
            url:'/storeUpQuestion?question_no=' + question_no,
        }).then((response) =>{          //这里使用了ES6的语法
            //console.log(response);       //请求成功返回的数据
        }).catch((error) =>{
            //console.log(error);      //请求失败返回的数据
        });
      },
      getQuestions(questionOffset, questionNum, updateTotalPage){
        console.log('condition',this.conditionForm);
        this.$axios({
          method:'post',
          url:'/api/get/Question',
          data:JSON.stringify({    //这里是发送给后台的数据
            questionOffset: questionOffset,
            questionNum: questionNum,
            conditionForm: this.conditionForm,
          }),
        }).then((response) =>{          //这里使用了ES6的语法
            console.log(response.data);
            if(updateTotalPage){
              this.totalPage = Math.floor(response.data.quantity/(this.row*this.col)) + 1; 
              console.log('update',this.totalPage);
            }
            this.curQuestions = response.data.questions;
        }).catch((error) =>{
            console.log(error);      //请求失败返回的数据
        });
      },
      updateCondition(newCondition){
        this.conditionForm = newCondition;
        //console.log(this.conditionForm);
        this.getQuestions(0, this.col*this.row*this.pageSize, true);
      }
    },
    created(){

      
    },
    mounted(){
    this.$nextTick(() => {
      // this.getQuestions(0, this.col*this.row*this.pageSize);
      //console.log(this.$refs);
      // for(let i=0; i < this.$refs.md.length; i++){
      //   this.$refs.md[i].$refs.vShowContent.style.background="#ffffff";
      //   this.$refs.md[i].$refs.vShowContent.style.lineHeight="200%";
      //   this.$refs.md[i].$refs.vShowContent.style.padding="0px";
      //   this.$refs.md[i].$refs.vShowContent.parentElement.parentElement.style.border="0px";
      //   this.$refs.md[i].$refs.vShowContent.parentElement.parentElement.parentElement.style.zIndex="0";
      // }
      // this.downloadAsPdf();
    });
  },
};
</script>

<style scoped>
  .pagination{
    margin-left: auto;
    margin-right: auto;
    text-align: center;
  }
  .text {
    font-size: 16px;
    text-align: center;
  }

  .item {
    background-color: #ffffff;
    margin-bottom: 18px;
  }

  .button{
    margin-left: 0px;
  }
  .time {
    font-size: 13px;
    color: #999;
    margin-right: 10px;
  }
  .image {
    width: 100%;
    display: block;
  }
  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  
  .clearfix:after {
      clear: both
  }
  .block {
    padding-top: 20px;
  }
  .card-footer{
    padding-top: 10px;
    width: 100%;
    float:left; 
  }
  .over{
    position:relative; 
    z-index:2;
    background-color: #ffffff;
  }
  .card{
    margin-right: 10px;
    margin-left:10px;
    line-height: 200%;
  }
</style>