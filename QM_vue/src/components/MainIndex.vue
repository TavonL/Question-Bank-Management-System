<template>
  <div>
  <el-row>
    <el-col :span="12"><div><p style="text-align:left; margin-left:50px">测试测试试题库</p></div></el-col>
    <el-col :span="12">
      <div style="margin-top:1em">
      <el-input placeholder="请输入内容" v-model="keyword" class="input-with-select">
        <el-select v-model="type" slot="prepend" placeholder="请选择">
          <el-option label="初中试题" value="1"></el-option>
          <el-option label="高中试题" value="2"></el-option>
          <el-option label="大学试题" value="3"></el-option>
        </el-select>
        <el-button slot="append" icon="el-icon-search" @click="search"></el-button>
      </el-input>
    </div>
    </el-col>
  </el-row>
  <el-row>
  <el-col :span="24"><div>
    <el-menu :default-active="activeIndex" class="el-menu-demo adjust" mode="horizontal" @select="handleSelect">
    <el-menu-item index="1">首页</el-menu-item>
    <el-submenu index="2">
      <template slot="title">试题库</template>
      <el-menu-item index="2-1">初中试题</el-menu-item>
      <el-menu-item index="2-2">高中试题</el-menu-item>
      <el-menu-item index="2-3">大学试题</el-menu-item>
    </el-submenu>
    <el-menu-item index="3">我的收藏</el-menu-item>
    <el-menu-item index="4">上传试题</el-menu-item>
    <el-menu-item index="5">自由组卷</el-menu-item>
    <el-menu-item index="6">个人信息</el-menu-item>
    <el-menu-item index="7" disabled>管理员后台</el-menu-item>
    </el-menu>
  </div></el-col>
  </el-row>
  </div>
</template>

<script>
export default {
  name: 'MainIndex',
  data () {
    return {
      activeIndex: '1',
      username: 'test',
      keyword: '',
      type: ''
    }
  },
  methods: {
    handleSelect (key, keypath) {
      var paths = ['/1', '/2', '/3', '/4', '/5','/6']
      console.log(keypath)
      this.$router.push({ path: paths[keypath[0] - 1] })
    },
    search () {
      alert(this.keyword)
    }
  }
}

</script>
<style scope>
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
