<template>
  <div>
  <el-input
  placeholder="输入关键字进行过滤"
  v-model="filterText">
</el-input>
    <el-tree
      :data="data"
      node-key="no"
      default-expand-all
      :expand-on-click-node="false"
      :render-content="renderContent"
      :filter-node-method="filterNode"
      ref="kpTree">
    </el-tree>
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
      }
    },
    watch: {
      filterText(val) {
        this.$refs.kpTree.filter(val);
      }
    },
    methods: {
      filterNode(value, data) {
        if (!value) return true;
        return data.label.indexOf(value) !== -1;
      },
      append(data) {
        const newChild = { no: 'add', label: 'testtest', children: [] };
        if (!data.children) {
          this.$set(data, 'children', []);
        }
        data.children.push(newChild);
      },

      remove(node, data) {
        const parent = node.parent;
        const children = parent.data.children || parent.data;
        const index = children.findIndex(d => d.no === data.no);
        children.splice(index, 1);
      },
      
      renderContent(h, { node, data, store }) {
        return (
          <span class="custom-tree-node">
            <span>{node.label}</span>
            <span>
              <el-button  type="text" on-click={ () => this.append(data) }disabled={data.no>=18||data.no==1}>添加类目</el-button>
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
.custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 20px;
    padding-right: 8px;
  }

</style>