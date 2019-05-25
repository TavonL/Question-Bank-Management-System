<template>
  <div>
  <el-row>
    <el-col :span="12"><div><p style="text-align:left; margin-left:50px">测试测试试题库</p></div></el-col>
  </el-row>
  <el-row>
  <el-col :span="24"><div>
    <el-menu :default-active="activeIndex" class="el-menu-demo adjust" mode="horizontal" @select="handleSelect">
    <el-submenu index="1">
      <template slot="title">试题库</template>
      <el-menu-item index="1-1">小学试题</el-menu-item>
      <el-menu-item index="1-2">初中试题</el-menu-item>
      <el-menu-item index="1-3">高中试题</el-menu-item>
    </el-submenu>
    <el-menu-item index="2">我的收藏</el-menu-item>
    <el-menu-item index="3">上传试题</el-menu-item>
    <el-menu-item index="4">自由组卷</el-menu-item>
    <el-menu-item index="5">个人信息</el-menu-item>
    <el-menu-item index="6" disabled>管理员后台</el-menu-item>
    </el-menu>
  </div></el-col>
  </el-row>
  </div>
</template>

<script>
export default {
  props: ['activeIndex'],
  data () {
    return {
      username: 'test',
      keyword: '',
      type: ''
    }
  },
  methods: {
    handleSelect (key, keypath) {
      var paths = ['/questionBank/', '/questionCollector', '/questionUpload', '/6', '/6','/6']
      console.log(keypath)
      if(keypath[0] == '1'){
        this.$router.push({ 
          path: paths[keypath[0] - 1] + keypath[1][2],
        });
      }
      else{
        this.$router.push({ path: paths[keypath[0] - 1] })
      }
    },
    search () {
      alert(this.keyword)
    }
  }
}

</script>
<style scoped>
.adjust{
  margin-top: 0px
}
.el-select .el-input {
  width: 100px;
}
.input-with-select .el-input-group__prepend {
  background-color: #fff;
}

</style>
