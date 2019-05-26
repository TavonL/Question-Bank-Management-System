<template>

  <div>
  <MainIndex activeIndex="4"></MainIndex>
    <el-row >
    <el-col :span="24" class="block">
    <div>
    <div class="block">
    <el-button
          type="danger"
          size="mini"
          @click="handleCancle()"
          v-if="addVisible">取消
    </el-button>
    <el-button
          type="success"
          size="mini"
          @click="handleAdd()"
          v-if="!addVisible">点击组卷
    </el-button>
    </div>
    </div>
    </el-col>
    </el-row>
 <div v-if="addVisible">
<PaperEditor @childFn="parentFn" ref="mychild"></PaperEditor>
 </div>  
<div v-if="!addVisible">
    <el-row gutter="10" v-for="o, i in row" :key="o" style="padding-top:20px">
    <el-col :span="2"><div><p></p></div></el-col>
    <el-col :span="5" v-for="o, i in col" :key="o">
      <el-card class="box-card" shadow="hover">
        <div slot="header" class="clearfix">
          <img :src="pics[o%1]" class="image">
        </div>
        <div class="item">
          <span class="text">试卷标题</span>
          <br>
          <div style="float:right">
            <time class="time">创建时间:2019.4.28</time>
            <el-button type="text" class="button">删除</el-button>
            <el-button type="text" class="button">查看</el-button>
          </div>
        </div>
      </el-card>
    </el-col>
    <el-col :span="2"><div><p></p></div></el-col>
    </el-row>
    <el-row>
    <el-col :span="24" class="block">  <div>
    <div class="block">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page.sync="current"
        :page-size="100"
        layout="prev, pager, next, jumper"
        :total="1000">
      </el-pagination>
    </div>
    </div>
    </el-col>
    </el-row>
    </div>
  </div>
</template>

<script>
import PaperEditor from '@/components/PaperEditor';
import MainIndex from '@/components/MainIndex';
import { mavonEditor } from 'mavon-editor'
import 'mavon-editor/dist/css/index.css'
export default {
    name:'TestPaperMake',
    components: {
            PaperEditor,
            mavonEditor,
            MainIndex
        },
    data(){
        
        return{
            qno:[],
            row: 5,
            col: 4,
            pics: [
              "https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1556457157&di=0eb2b58e7ff9b2b525c889a7310bc669&src=http://d.hiphotos.baidu.com/zhidao/pic/item/d043ad4bd11373f0d965c83fa50f4bfbfbed0433.jpg"
            ],
            current:1,
            addVisible: false,
            confirmVisible: false,
            paperForm:{
              titleMd:'',
              questionList:[],
            },
            data: [{
          id: 1,
          label: '一级 1',
          children: [{
            id: 4,
            label: '二级 1-1',
            
          }]
        }, {
          id: 2,
          label: '一级 2',
          children: [{
            id: 5,
            label: '二级 2-1'
          }, {
            id: 6,
            label: '二级 2-2'
          }]
        }, {
          id: 3,
          label: '一级 3',
          children: [{
            id: 7,
            label: '二级 3-1'
          }, {
            id: 8,
            label: '二级 3-2',
            
          }]
        }],
        defaultProps: {
          children: 'children',
          label: 'label'
        }
      };
    },
    methods: {
      handleSizeChange(val) {
        console.log(`每页 ${val} 条`);
      },
      handleCurrentChange(val) {
        console.log(`当前页: ${val}`);
      },
      handleAdd(){
          this.addVisible=true;

      },
      handleCancle(){
        this.addVisible=false;
      },
      parentFn(qno){
        this.qno=qno.slice(0);
      },
      
       
    }   
};
</script>

<style>

 .text {
    font-size: 16px;
    align-content: center;
  }

  .item {
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
</style>