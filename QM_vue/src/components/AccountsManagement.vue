<template>
<div>
  <el-table
    :data="tableData"
    style="width: 100%">
    <el-table-column
      align="center"
      label="用户名"
      prop="userName"
      width='300px'>
      <template slot-scope="scope" >
        <el-input v-model="scope.row.userName" placeholder="请输入内容" v-if='scope.row.infoChangeSeen'></el-input>
        <span v-if='!scope.row.infoChangeSeen'>{{ scope.row.userName }}</span>
      </template>
    </el-table-column>
    <el-table-column
      align="center"
      label="用户密码"
      prop="password"
      width='300px'>
      <template slot-scope="scope" >
        <el-input v-model="scope.row.password" placeholder="请输入内容" v-if='scope.row.infoChangeSeen'></el-input>
        <span v-if='!scope.row.infoChangeSeen'>{{ scope.row.password }}</span>
      </template>
    </el-table-column>
     <el-table-column
      align="center"
      label="权限类别"
      prop="permission"
      width='200px'>
       <template slot-scope="scope" >
        <el-select v-model="scope.row.permission" placeholder="请输入内容" v-if='scope.row.infoChangeSeen' style="width:180px;">
        <el-option
          v-for="item in options"
          :key="item.value"
          :value="item.value">
        </el-option>
        </el-select>
        <span v-if='!scope.row.infoChangeSeen'>{{ scope.row.permission }}</span>
      </template>
    </el-table-column>
    <el-table-column align="center" width='80px'>
     <template slot="header" slot-scope="scope">
      <el-button
          type="success"
          size="mini"
          @click="handleAdd()">添加</el-button>
      </template>
      </el-table-column>
    <el-table-column
      align="right">
      <template slot="header" slot-scope="scope">
      <el-input
          v-model="search"
          size="mini"
          placeholder="输入关键字搜索"
          @input="handleFilter"/>
  </template>
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="handleEdit(scope.$index, scope.row)">{{scope.row.changeButton}}</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="handleDelete(scope.$index, scope.row)"
          :disabled="scope.row.disabled">删除</el-button>
      </template>
    </el-table-column>
     
  </el-table>
  <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page.sync="currentPage"
      :page-sizes="[5, 10, 20,50 ]"
      :page-size="pageSize"
      layout="total,sizes, prev, pager, next, jumper"
      :total="totalRecords">
    </el-pagination>
  </div>
</template>

    

<script>
import axios from 'axios';
  var usersData=[];      
  export default {
    name:'AccountsManagement',
    data() {
      return {
        tableData: usersData.slice(0,5),
        filterData: usersData,
        search: '',
        currentPage: 1,
        pageSize: 5,
        totalRecords: usersData.length,
         options: [{
          value: '试题管理员',
        }, {
          value: '试题录入员',
        }, {
          value: '超级用户',
        }],
        value: '',
        
      }
    },
    methods: {
      handleAdd() {
        if(this.search!='')
        {
          this.$message({
            type: 'error',
            message: '请清空筛选栏'
          }); 
          return;
        }
        usersData.unshift(
          {
            userName: '',
            password: '',
            permission: '试题管理员',
            infoChangeSeen: true,
            changeButton: '完成',
            lastUserName:'',
            disabled:true,
          }
        )
        this.handleFilter();
      },
      handleEdit(index, row) {
        if(row.changeButton=="编辑"){
          this.tableData[index].infoChangeSeen=true;
          this.tableData[index].changeButton="完成";
          this.tableData[index].lastUserName=this.tableData[index].userName;
          this.tableData[index].disabled=true;
        }else{
          if( this.tableData[index].userName=== ''){
            this.$message({
            type: 'error',
            message: '用户名不能为空！'
          }); 
          return;      
          }
          if( this.tableData[index].password=== ''){
            this.$message({
            type: 'error',
            message: '密码不能为空！'
          }); 
          return;      
          }
          if( /^[A-z]\w$/.test(this.tableData[index].userName)){
            //错误待改
            this.$message({
            type: 'error',
            message: '用户名不规范，必须字母开头且不包含非法字符！'
          }); 
          return;      
          }
          if( /^\w$/.test(this.tableData[index].password)){
            //错误待改
            this.$message({
            type: 'error',
            message: '密码不规范，不能包含非法字符！'
          }); 
          return;      
          }
          for(var i = 0;i<usersData.length;i++){
            if( this.tableData[index].userName==usersData[i].userName&&this.tableData[index].lastUserName!=usersData[i].lastUserName){
            this.$message({
            type: 'error',
            message: '数据库中用户名数据重复！'+this.tableData[index].userName+'test'+this.tableData[index].lastUserName+usersData[i].userName,
            }); 
          return;      
            }
          }
          if(this.tableData[index].lastUserName===''){
            this.tableData[index].lastUserName='none';
            this.$axios({
        method:'post',
        url:'/api/auth/uploadUserMsg',
        data:JSON.stringify({    //这里是发送给后台的数据
            userName : this.tableData[index].userName,
	          password : this.tableData[index].password,
	          permission : this.tableData[index].permission,
	          opt : "add",
	          lastUserName: "none"
          }),
      }).then((response) => {


      }).catch((error) => {
        alert(error);
      });
          }
           this.$axios({
        method:'post',
        url:'/api/auth/uploadUserMsg',
        data:JSON.stringify({    //这里是发送给后台的数据
            userName : this.tableData[index].userName,
	          password : this.tableData[index].password,
	          permission : this.tableData[index].permission,
	          opt : "update",
	          lastUserName: this.tableData[index].lastUserName,
          }),
      }).then((response) => {


      }).catch((error) => {
        alert(error);
      });
          

          this.tableData[index].infoChangeSeen=false;
          this.tableData[index].changeButton="编辑";
          this.tableData[index].disabled=false;
          //this.usersData[this.pageSize*(this.currentPage-1)+index]=this.tableData[index];
          //数据库用户表单条修改，添加操作,

          this.$message({
            type: 'success',
            message: '修改成功！'
            }); 
        }
        
        
      },
      handleDelete(index, row) {
        this.$confirm('此操作将删除该记录, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.$message({
            type: 'success',
            message: '删除成功!'
          });
          //数据库用户表删除操作
        //usersData.splice(this.pageSize*(this.currentPage-1)+index,1);
        var delData=this.filterData.splice(this.pageSize*(this.currentPage-1)+index,1);
        this.$axios({
        method:'post',
        url:'/api/auth/uploadUserMsg',
        data:JSON.stringify({    //这里是发送给后台的数据
            userName : delData[0].userName,
	          password : delData[0].password,
	          permission : delData[0].permission,
	          opt : "del",
	          lastUserName: delData[0].lastUserName,
          }),
      }).then((response) => {


      }).catch((error) => {
        alert(error);
      });
        for(var i =0 ;i<usersData.length;i++)
        {
          if(delData[0].userName==usersData[i].userName)
          {
            usersData.splice(i,1);
            break;
          }
        }
        var a=(this.currentPage-1)*this.pageSize;
        if(a+this.pageSize>this.filterData.length){
          this.tableData=this.filterData.slice(a,this.filterData.length);
        }else{
          this.tableData=this.filterData.slice(a,a+this.pageSize);
        }
         this.totalRecords=this.filterData.length;
        

        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
        
      },
      handleFilter(){
        //错误需要处理，filter创建副本，直接赋值不创建副本！！
        this.filterData=usersData.filter((data) => !this.search || data.permission.toLowerCase().includes(this.search.toLowerCase())||data.userName.toLowerCase().includes(this.search.toLowerCase()));
        this.currentPage=1;
        this.totalRecords=this.filterData.length;
        this.tableData=this.filterData.slice(0,this.pageSize);
      },
       handleSizeChange(val) {
        this.pageSize = val;
        this.currentPage = 1;
        if(val>this.totalRecords){
          this.tableData=this.filterData.slice(0,this.totalRecords);
        }else{
          this.tableData=this.filterData.slice(0,val);
        }
        
      },
      handleCurrentChange(val) {
        var size=this.pageSize;
        var a=(val-1)*size;
        if((a+size)>this.totalRecords){
          this.tableData=this.filterData.slice(a,this.totalRecords);
        }else{
          this.tableData=this.filterData.slice(a,a+size);
        }
      },
      
      getUsersDataFromBackend(){
        var that = this;
        const path = '/api/auth/getUsersMsg';
          axios.get(path).then(function (response) {
            var msg = response.data;
            usersData=msg;
            that.tableData=usersData.slice(0,5);
            that.handleFilter();
            that.totalRecords = usersData.length;
          }).catch(function (error) {
            usersData=[{
              userName: 'admin1',
              password: 'admin1',
              permission: '管理员',
              infoChangeSeen: false,
              changeButton: '编辑',
              id:-1
            }];
            that.tableData=usersData.slice(0,5);
            that.filterData=usersData;
            alert(error);
          })
      },
    },
    created () {
        this.getUsersDataFromBackend();
      }
  }
</script>
<style>
.headerRow {
    
  }
</style>