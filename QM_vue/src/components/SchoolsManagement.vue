<template>
  <div>
  <el-input
  placeholder="输入关键字进行过滤"
  v-model="filterText">
</el-input>
    <el-tree class="tree"
      :data="data"
      node-key="no"
      default-expand-all
      :expand-on-click-node="false"
      :render-content="renderContent"
      :filter-node-method="filterNode"
      ref="school">
    </el-tree>
    <el-dialog title="添加学校" :visible.sync="dialogFormVisible">
  <el-form :model="form">
    <el-form-item label="学校名称" :label-width="formLabelWidth">
      <el-input v-model="form.name" auto-complete="off"></el-input>
    </el-form-item>
    <el-form-item label="学校性质" :label-width="formLabelWidth">
      <el-select v-model="form.prop" placeholder="请选择活动区域">
        <el-option label="公立" value="公立"></el-option>
        <el-option label="私立" value="私立"></el-option>
      </el-select>
    </el-form-item>
  </el-form>
  <div slot="footer" class="dialog-footer">
    <el-button @click="dialogFormVisible = false">取 消</el-button>
    <el-button type="primary" @click="submitForm">确 定</el-button>
  </div>
</el-dialog>
    
  </div>
</template>

<script>
    let id = 1000;
    import axios from 'axios';
export default {
    name:'SchoolsManagement',
    data() { 
      return {
        data: '',
        filterText: '',
        form:{
          name:'',
          prop:'',
        },
        dialogFormVisible:false,
        addData:'',
        delData:'',
        node:'',
      }
    },
    watch: {
      filterText(val) {
        this.$refs.schoolTree.filter(val);
      }
    },
    methods: {
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      append(node,data) {
        this.addData=data;
        this.node=node;
        this.dialogFormVisible=true;
        
      },
      submitForm(){
        this.dialogFormVisible=false;

        this.$axios({
        method:'post',
        url:'/api/upload/Schools',
        data:JSON.stringify({    //这里是发送给后台的数据
            school_name : this.form.name,
	          school_nature : this.form.prop,
	          parent_no : this.node.data.no,
	          opt : "add",
          }),
      }).then((response) => {
        this.getSchoolsFromBackend()


      }).catch((error) => {
        alert(error);
      });
        //const newChild = { no: 'add', label: 'testtest' };
        //if (!data.children) {
          //this.$set(data, 'children', []);
        //}
        //data.children.push(newChild);


      },
      remove(node, data) {
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
       const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.no === data.no);
        var deldata=children.splice(index, 1);
        this.$axios({
        method:'post',
        url:'/api/upload/Schools',
        data:JSON.stringify({    //这里是发送给后台的数据
            school_name : deldata[0].label,
	          school_nature : '',
	          parent_no : deldata[0].no,
	          opt : "del",
          }),
      }).then((response) => {
        


      }).catch((error) => {
        alert(error);
      });


        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
        
      },
      
      renderContent(h, { node, data, store }) {
        return (
          <span class="custom-tree-node">
            <span>{node.label}</span>
            <span>
              <el-button  type="text" on-click={ () => this.append(node, data) }disabled={data.no>=18||data.no==1}>添加类目</el-button>
              <el-button  type="text" on-click={ () => this.remove(node, data)} disabled={data.no<18}>删除</el-button>
            </span>
          </span>);
      },
      getSchoolsFromBackend(){
        var that = this;
        const path = '/api/get/SourcesNo';
          axios.get(path).then(function (response) {
            var msg = response.data;
            that.data=msg;
          }).catch(function (error) {
            alert(error);
          })
      }
    },
    created() {
      this.getSchoolsFromBackend();
    },
};
</script>

<style>
.tree{
  margin-top:1%;
}
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
    line-height:200%;
  }

</style>