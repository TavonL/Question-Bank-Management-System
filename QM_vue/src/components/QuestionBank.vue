<template>
  <div>
    <MainIndex activeIndex="2"></MainIndex>
    <!-- <p>test</p> -->
    <SubSearch></SubSearch>
    <div class="block pagination">
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page.sync="currentPage"
        :page-size="100"
        layout="prev, pager, next, jumper"
        :total="1000">
      </el-pagination>
    </div>
    <el-row :gutter="10" v-for="o, i in row" :key="o" style="padding-top:20px">
    <el-col :span="2"><div><p></p></div></el-col>
    <el-col :span="5" v-for="(question, index) in curQuestions.slice(i*col,(i+1)*col)" :key="index">
      <el-card class="box-card" shadow="hover" >
        <div slot="header" class="clearfix">
          <img :src="question.figure_url" class="image">
        </div>
        <div class="item">
          <div style="height:165px; z-index:0">
          <mavon-editor ref="md" class="inner-block mavon-editor"
          :subfield="false" defaultOpen="preview" :toolbarsFlag="false" :boxShadow="false"
          v-model="question.question_content"
          placeholder="缺少题干"
          :editable="false"/>
          </div>
          <div class="card-footer over" >
            <time class="time">试题来源：{{question.paper_name}}</time>
            <el-button type="text" class="button" @click.prevent="readMore(question)">查看详情</el-button>
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
        :total="1000">
      </el-pagination>
    </div>
  </div>
</template>

<script>
import SubSearch from '@/components/SubSearch';
import MainIndex from '@/components/MainIndex';
export default {
    name:'QuestionBank',
    components:{SubSearch, MainIndex},
    data(){
        return{
            row: 5,
            col: 4,
            curQuestions: [{
              quetison_no: 123,
              question_content: '测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下测试一下',
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
            
        }
    },
    methods: {
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);

        if((this.currentPage-1) % 10 != 0)
          return;
        this.$axios({
              method:'get',
              url:'/getQuestions?question_offset='+ (this.currentPage-1) + '&question_num='+ (this.col*this.row*10),
          }).then((response) =>{          //这里使用了ES6的语法
              console.log(response);       //请求成功返回的数据
          }).catch((error) =>{
              console.log(error);      //请求失败返回的数据
          });
      },
      readMore(question){

      },
      storeUp(question_no){
        this.$axios({
            method:'get',
            url:'/storeUpQuestion?question_no=' + question_no,
        }).then((response) =>{          //这里使用了ES6的语法
            console.log(response);       //请求成功返回的数据
        }).catch((error) =>{
            console.log(error);      //请求失败返回的数据
        });
      },
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
      this.$axios({
          method:'get',
          url:'/getQuestions?question_offset=0&question_num='+ (this.col*this.row*10),
        }).then((response) =>{          //这里使用了ES6的语法
          console.log(response);       //请求成功返回的数据
        }).catch((error) =>{
          console.log(error);      //请求失败返回的数据
        });
    },
    mounted(){
    this.$nextTick(() => {
      console.log(this.$refs);
      for(let i=0; i < this.$refs.md.length; i++){
        this.$refs.md[i].$refs.vShowContent.style.background="#ffffff";
        this.$refs.md[i].$refs.vShowContent.style.lineHeight="200%";
        this.$refs.md[i].$refs.vShowContent.style.padding="0px";
        this.$refs.md[i].$refs.vShowContent.parentElement.parentElement.style.border="0px";
        this.$refs.md[i].$refs.vShowContent.parentElement.parentElement.parentElement.style.zIndex="0";
      }
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
</style>