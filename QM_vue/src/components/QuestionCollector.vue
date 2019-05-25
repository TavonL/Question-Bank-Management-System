<template>
  <div> 
    <MainIndex activeIndex="2"></MainIndex>
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
    <el-col :span="10" v-for="(question, index) in curQuestions.slice(i*col,(i+1)*col)" :key="index">
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
            <el-button type="text" class="button" @click.prevent="storeUp(question.question_no)">收藏</el-button>
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

import MainIndex from '@/components/MainIndex';
import QuestionDetail from '@/components/QuestionDetail';
export default {
    name:'QuestionBank',
    components:{ MainIndex, QuestionDetail},
    data(){
        return{
            conditionForm:{},
            question_no: 123,
            question_index: 0,
            questionDetailsVisible: false,
            row: 5,
            col: 2,
            pageSize: 10,
            curQuestions: [{
              quetison_no: 123,
              question_content: '<p>测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下试一下测试一下测试试一下测试一下测试试一下测试一下测试试一下测试一下测试试一下测试一下测试试一下测试一下测试试一下测试一下测试</p>',
              figure_url:"https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1556457157&di=0eb2b58e7ff9b2b525c889a7310bc669&src=http://d.hiphotos.baidu.com/zhidao/pic/item/d043ad4bd11373f0d965c83fa50f4bfbfbed0433.jpg",
              paper_name: '上海大学2019大学三年级微积分期末卷',
            },{
              question_content: '测试一下',
              figure_url:"https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1556457157&di=0eb2b58e7ff9b2b525c889a7310bc669&src=http://d.hiphotos.baidu.com/zhidao/pic/item/d043ad4bd11373f0d965c83fa50f4bfbfbed0433.jpg",
              paper_name: '上海大学2019大学三年级微积分期末卷',
            },{
              question_content: '测试一下',
              figure_url:"https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1556457157&di=0eb2b58e7ff9b2b525c889a7310bc669&src=http://d.hiphotos.baidu.com/zhidao/pic/item/d043ad4bd11373f0d965c83fa50f4bfbfbed0433.jpg",
              paper_name: '上海大学2019大学三年级微积分期末卷',
            },{
              question_content: '测试一下',
              figure_url:"https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1556457157&di=0eb2b58e7ff9b2b525c889a7310bc669&src=http://d.hiphotos.baidu.com/zhidao/pic/item/d043ad4bd11373f0d965c83fa50f4bfbfbed0433.jpg",
              paper_name: '上海大学2019大学三年级微积分期末卷',
            },{
              question_content: '测试一下',
              figure_url:"https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1556457157&di=0eb2b58e7ff9b2b525c889a7310bc669&src=http://d.hiphotos.baidu.com/zhidao/pic/item/d043ad4bd11373f0d965c83fa50f4bfbfbed0433.jpg",
              paper_name: '上海大学2019大学三年级微积分期末卷',
            }],
            pics: [
              "https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1556457157&di=0eb2b58e7ff9b2b525c889a7310bc669&src=http://d.hiphotos.baidu.com/zhidao/pic/item/d043ad4bd11373f0d965c83fa50f4bfbfbed0433.jpg"
            ],
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
        this.getQuestions(Math.floor((val-1)/10) * this.col * this.row, this.col*this.row*pageSize);
        //console.log(Math.floor((val-1)/10) * this.col * this.row);
        
      },
      readMore(question_no, index){
        this.question_no = question_no;
        this.questionDetailsVisible = true;
        this.question_index = index + 1;
      },
      nextQuestion(){
        if(this.curQuestions.length < this.question_index){
          return;
        }
        this.question_no = this.curQuestions[this.question_index].question_no;
        this.question_index += 1;
        if(this.question_index % (this.col * this.row)){
          this.currentPage += 1;
          if((this.currentPage-1) % 10 == 0){
            this.question_index = 0;
            handleCurrentChange(this.currentPage);
          }
          
        }
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
        //console.log('condition',this.conditionForm);
        this.$axios({
          method:'post',
          url:'/api/get/Question',
          data:this.qs.stringify({    //这里是发送给后台的数据
            questionOffset: questionOffset,
            questionNum: questionNum,
            conditionForm: this.conditionForm,
          })
        }).then((response) =>{          //这里使用了ES6的语法
            //console.log(response);       //请求成功返回的数据
            if(updateTotalPage){
              this.totalPage = 1000; //待改
            }

        }).catch((error) =>{
            //console.log(error);      //请求失败返回的数据
        });
      },
      updateCondition(newCondition){
        this.conditionForm = newCondition;
        //console.log(this.conditionForm);
        this.getQuestions(0, this.col*this.row*this.pageSize);
      }
    },
    created(){

      this.getQuestions(0, this.col*this.row*this.pageSize);
    },
    mounted(){
    this.$nextTick(() => {
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