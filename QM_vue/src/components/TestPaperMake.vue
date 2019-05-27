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
<PaperEditor @childFn="parentFn"  v-if="addVisible"></PaperEditor>  
  <div v-if="!addVisible">
   <el-table
    :data="paperList"
    class='table'>
    <el-table-column
      label="日期"
      width="500"
      align="center">
      <template slot-scope="scope">
        <span style="margin-left: 10px">{{ scope.row.createdDate }}</span>
      </template>
    </el-table-column>
    <el-table-column
      label="标签"
      width="500"
      align="center">
      <template slot-scope="scope">
        <span style="margin-left: 10px">{{ scope.row.key }}</span>
      </template>
    </el-table-column>
    <el-table-column label="操作" align="center">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleCheck(scope.$index)">查看</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index)">删除</el-button>
      </template>
    </el-table-column>
  </el-table>
  <el-dialog
  title="查看"
  :visible.sync="dialogVisible"
  width="80%">
  <MakedPaperPreview ></MakedPaperPreview >

</el-dialog>
    </div>
  </div>
</template>
<script>
import MakedPaperPreview from '@/components/MakedPaperPreview';
import PaperEditor from '@/components/PaperEditor';
import MainIndex from '@/components/MainIndex';
import Dicts from '@/global/Dicts';
export default {
    name:'TestPaperMake',
    components: {
            PaperEditor,
            MainIndex,
            MakedPaperPreview
        },
    data(){
        
        return{
            addVisible: false, 
            paperList:[],  
            dialogVisible:false,      
      };
    },
    methods: {
      handleAdd(){
          this.addVisible=true;
      },
      handleCancle(){
        this.addVisible=false;
      },
      parentFn(str,paperInfo){
        
        var myDate = new Date();
        var paperItem={
          key:str,
          createdDate:paperInfo.createdDate,
          createdTime:myDate.toLocaleString(),
          paperInfo:paperInfo,
        } 
        this.paperList.push(paperItem);
        localStorage.setItem('paperList', JSON.stringify(this.paperList));

        this.addVisible=false;
      },
      handleCheck(index){
        var questions = JSON.parse(localStorage.getItem(this.paperList[index].key));
        var paperInfo = this.paperList[index].paperInfo
        sessionStorage.getItem("MakedPaperQuestions",JSON.stringify(questions));
        sessionStorage.setItem('MakedPaperInfo', JSON.stringify(paperInfo));
        this.dialogVisible=true;
      },
      handleDelete(index){
        
        localStorage.removeItem(this.paperList[index].key);
        this.paperList.splice(index,1);
        localStorage.setItem('paperList', JSON.stringify(this.paperList));
        if(this.paperList.length==0){
          localStorage.removeItem("paperList");
        }
      },
    

    },
    created() {
      if(localStorage.getItem("paperList")!==null){
        this.paperList=JSON.parse(localStorage.getItem("paperList"));
      }
    },
};
</script>

<style>

.table{
  width: 90%;
    margin-left: auto; 
    margin-right: auto;
}
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
  .box-card {
    width: 90%;
    margin-left: auto; 
    margin-right: auto;
    margin-top: 50px;
    margin-bottom: 50px;
  }
</style>