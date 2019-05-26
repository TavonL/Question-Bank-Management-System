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
    name:'KPManagement',
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
              <el-button  type="text" on-click={ () => this.append(data) }>添加类目</el-button>
              <el-button  type="text" on-click={ () => this.remove(node, data)} disabled={data.no<10}>删除</el-button>
            </span>
          </span>);
      },
      getKPFromBackend(){
        var that = this;
        const path = '/api/get/KnowledgePoints';
          axios.get(path).then(function (response) {
            // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串
            // 可以直接通过 response.data 取key-value
            // 坑一：这里不能直接使用 this 指针，不然找不到对象
            var msg = response.data;
            // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串
            //that.data=JSON.parse(JSON.stringify(msg))
            that.data=msg;
            //that.outputObj(that.data[0]);
          }).catch(function (error) {
            alert(error);
          })
      }
    },
    created() {
      this.getKPFromBackend();
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