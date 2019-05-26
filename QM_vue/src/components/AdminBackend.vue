<template>
  <div>
    <MainIndex activeIndex="6"></MainIndex>
  <el-tabs type="card" tab-position="left">
  <el-tab-pane label="用户管理">
    <AccountsManagement></AccountsManagement>
  </el-tab-pane>
  <el-tab-pane label="学校管理">
  <SchoolsManagement></SchoolsManagement>
  </el-tab-pane>
  <el-tab-pane label="知识点管理">
  <KPManagement></KPManagement>
  </el-tab-pane>
</el-tabs>
    
  </div>
</template>

<script>
import AccountsManagement from '@/components/AccountsManagement';
import KPManagement from '@/components/KPManagement';
import SchoolsManagement from '@/components/SchoolsManagement';
import MainIndex from '@/components/MainIndex';
export default {
    name:'AdminBackend',
    components: {
            AccountsManagement,
            KPManagement,
            MainIndex,
            SchoolsManagement
        },
    data(){
        
        return{
            qno:[],
            
      };
    },
    methods: {
      
       
    }   
};
</script>

<style>


</style>