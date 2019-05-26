<template>
<div>
<div class='stepcard'>
<el-card class="box-card">
<el-steps :active="curstep">
  <el-step title="步骤 1" description="基础信息编辑"></el-step>
  <el-step title="步骤 2" description="题目信息编辑"></el-step>
  <el-step title="步骤 3" description="题目顺序编辑"></el-step>
  <el-step title="步骤 4" description="预览试卷"></el-step>
</el-steps>
<el-button  class='nextButton'  type="primary" round @click="handleQuestionCreate()" v-if='step1Visible'>下一步</el-button>
<el-button  class='nextButton'  type="danger" round @click="handlePeriorStep1()" v-if='step2Visible'>上一步</el-button>
<el-button  class='nextButton'  type="primary" round @click="handleQuestionAdjust()" v-if='step2Visible'>下一步</el-button>
<el-button  class='nextButton'  type="danger" round @click="handlePeriorStep2()" v-if='step3Visible'>上一步</el-button>
<el-button  class='nextButton'  type="primary" round @click="handlePaperpreview()" v-if='step3Visible'>下一步</el-button>
</el-card>
</div>

<div class='step1' v-if='step1Visible'>
<el-card class="box-card">

  <div slot="header" class="clearfix">
    <span>基础信息</span>
  </div>

<el-form :inline="true" :model="form1">
    <el-form-item label="学校" >
      <el-cascader
    expand-trigger="hover"
    :options="schoolOptionsCas"
    :show-all-levels="false"
    v-model="form1.school">
  </el-cascader>
    </el-form-item>
    <el-form-item label="科目" >
      <el-select v-model="form1.subject" placeholder="请选择科目" style="width:180px;" @change="handleKPOptionsCas">
        <el-option
          v-for="item in subjectOptions"
          :key="item.value"
          :label="item.label"
          :value="item.value"
          :disabled="item.disabled">
        </el-option>
      </el-select>
    </el-form-item>
    <el-form-item label="年级">
    <el-cascader
    expand-trigger="hover"
    :options="gradeOptions"
    :show-all-levels="false"
    v-model="form1.grade">
       </el-cascader> 
    </el-form-item>
    <el-form-item label="总分">
      <el-input  v-model.number="form1.mark" autocomplete="off" style="width:150px;"></el-input>
    </el-form-item>
    <el-form-item label="自动组题">
    <el-switch v-model="form1.auto"></el-switch>
  </el-form-item>
    </el-form>  
    </el-card>

  <!-- 题型编辑 相关数据结构formkey--> 
<el-card class="box-card">

  <div slot="header" class="clearfix">
    <span>题型编辑</span>
    <el-button style="float: right; padding: 3px 0" type="text" @click="handleAddQuestionType()">添加题型</el-button>
  </div>

  <div class="block">
  <el-form :model="formkey1">
  <el-form-item label="学校限定" >
    <el-radio-group v-model="formkey1.schoolTagVisible">
    <el-radio :label="false">不限</el-radio>
    <el-radio :label="true">限定</el-radio>
  </el-radio-group>

  <div v-if='formkey1.schoolTagVisible'>
  <el-form :model='schoolform' :inline="true">
  <el-form-item 
    label="省/直辖市" 
    :rules="[{ required: true, message: '必填', trigger: 'blur' },]">
  <el-select
    v-model="schoolform.provinces"
    multiple
    filterable
    allow-create
    default-first-option
    placeholder="省/直辖市，必填"
    @change='handlePOptionsChange'
    >
    <el-option
      v-for="item in provinceOptions"
      :key="item.value"
      :label="item.label"
      :value="item.no">
    </el-option>
  </el-select>
  </el-form-item>
  <el-form-item label='市'>
  <el-select
    v-model="schoolform.citys"
    multiple
    filterable
    allow-create
    default-first-option
    placeholder="市，选填"
    @change='handleCOptionsChange'>
    <el-option
      v-for="item in cityOptions"
      :key="item.value"
      :label="item.label"
      :value="item.no">
    </el-option>
  </el-select>
  </el-form-item>
  <el-form-item label='区/县'>
  <el-select
    v-model="schoolform.countys"
    multiple
    filterable
    allow-create
    default-first-option
    placeholder="区/县，选填"
    @change='handleCoOptionsChange'>
    <el-option
      v-for="item in countyOptions"
      :key="item.value"
      :label="item.label"
      :value="item.no">
    </el-option>
  </el-select>
  </el-form-item>
  <el-form-item label='学校'>
  <el-select
    v-model="schoolform.schools"
    multiple
    filterable
    allow-create
    default-first-option
    placeholder="学校，选填">
    <el-option
      v-for="item in schoolOptions"
      :key="item.value"
      :label="item.label"
      :value="item.no">
    </el-option>
  </el-select>
  </el-form-item>
  </el-form>
</div>
    </el-form-item>
    <el-form-item label="学校性质限定" >
    <el-radio-group v-model="formkey1.prop">
    <el-radio :label="0">不限</el-radio>
    <el-radio :label="1">公立</el-radio>
    <el-radio :label="2">私立</el-radio>
  </el-radio-group>
    </el-form-item>
    <el-form-item label="知识点限定" >
    <el-radio-group v-model="formkey1.knowledgeTagVisible">
    <el-radio :label="false">不限</el-radio>
    <el-radio :label="true">限定</el-radio>
    </el-radio-group>

    <div v-if='formkey1.knowledgeTagVisible'>
    <el-select
    v-model="formkey1.knowledgeTags"
    multiple
    filterable
    allow-create
    default-first-option
    placeholder="请选择"
    style='width:100%;'>
    <el-option
      v-for="item in KPOptions"
      :key="item.value"
      :label="item.label"
      :value="item.no">
    </el-option>
  </el-select>
</div>

    </el-form-item>
  </el-form>
</div>

  <el-form :inline="true" :model="selectedTypes">

  <div v-for="i in selectedTypes">
  <el-form-item label="题型" class='qinput'>
      <el-select v-model="i.type"  placeholder="请选择">
            <el-option
          v-for="item in qTypeOptions"
          :key="item.value"
          :value="item.value"
          :label='item.label'
          :disabled="item.disabled">
    </el-option>
    </el-select>
  </el-form-item>
  <el-form-item label="题目数量" class='qinput'>
      <el-input v-model.number="i.qnum" placeholder="请输入" class='qinput1'></el-input>
  </el-form-item>
  <el-form-item label="每题分数" class='qinput'>
      <el-input v-model.number="i.point" placeholder="请输入" class='qinput1'></el-input>
  </el-form-item>
  <el-form-item label="最小难度系数" class='qinput'>
      <el-rate
        class="rate"
        v-model="i.minDiffiDegree"
        :max="3"
        show-text
        text-color="#ff9900"
        :texts="['简单','中等','难']">
      </el-rate>
  </el-form-item>
  <el-form-item label="最大难度系数" class='qinput'>
      <el-rate
        class="rate"
        v-model="i.maxDiffiDegree"
        :max="3"
        show-text
        text-color="#ff9900"
        :texts="['简单','中等','难']">
      </el-rate>
  </el-form-item>
  <el-button
      type="text"
      style="float: right; padding: 3px 0"
      @click="removeType(i.id)">
      删除
    </el-button>
  </div>
  </el-form>
</el-card>
</div>
<el-dialog
    title="查看详情"
    :visible.sync="questionDetailsVisible"
    width="80%">
      <QuestionDetail :questionNo="q_no"></QuestionDetail>
      <span slot="footer" class="dialog-footer">
        <el-button type="default" @click.prevent="questionDetailsVisible = false">关闭</el-button>
      </span>
    </el-dialog>
  <div style="text-align: center" v-if='step2Visible' class='step2'>
  
<el-card class="box-card">
  <div slot="header" class="clearfix">
    <span>题目选择</span>
  </div>
    <el-transfer
      style="text-align: left; display: inline-block;"
      v-model="qno"
      filterable
      :titles="['可选题目', '已选题目']"
      :format="{
        noChecked: '${total}',
        hasChecked: '${checked}/${total}'
      }"
      @change="handleChange"
      :data="data">
      <span slot-scope="{ option }">
      <el-row>
      <el-col><span style='position:relative;bottom:3px;'>{{option.type}}-</span><el-button type="text" size='medium' style='position:relative;bottom:3px;' @click="q_no=option.key;questionDetailsVisible=true;">{{option.label}}</el-button><span style='position:relative;bottom:1px;'></span></el-col>
      </el-row>
      </span> 
    </el-transfer>
    </el-card >
    <el-card class="box-card">
  <div slot="header" class="clearfix">
    <span>试题抬头</span>
  </div>
    <el-input v-model='paperTitle'placeholder='请输入试题抬头'></el-input>
    </el-card >
</div>
 <div style="text-align: center" v-if='step3Visible' class='step3'>
<el-card class="box-card">
<div slot="header" class="clearfix">
    <span>题型顺序调整</span>
  </div>

<el-tree
  :data="qdata"
  node-key="id"
  default-expand-all
  @node-drag-start="handleDragStart"
  @node-drag-enter="handleDragEnter"
  @node-drag-leave="handleDragLeave"
  @node-drag-over="handleDragOver"
  @node-drag-end="handleDragEnd"
  @node-drop="handleDrop"
  draggable
  :allow-drop="allowDrop"
  :allow-drag="allowDrag">
  </el-tree>
    </el-card >
</div>
<div class='step4' v-if='step4Visible'>
<MakedPaperPreview></MakedPaperPreview >
</div>
 </div>   
</template>
<script>
import Dicts from '@/global/Dicts';
import MakedPaperPreview from '@/components/MakedPaperPreview'
import axios from 'axios';
import QuestionDetail from '@/components/QuestionDetail';


export default {
    name:'PaperEditor',
    components: {
            MakedPaperPreview,
            QuestionDetail,
        },
    
    data(){
      var subjectOpts=Dicts.subjectOpts.slice(0);
      var gradeOpts=Dicts.gradeOpts.slice(0);
      var typeOpts=Dicts.typeOpts.slice(0);
      subjectOpts[0]['disabled']=true;
      typeOpts[0]['disabled']=true;
      gradeOpts[0]['disabled']=true;

      
        return{
          q_no:'2',
          qdata:[],
          qsdata: [{
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
        curstep:1,
        paperTitle:'',
        form1: {
                school: [],
                subject:'',
                mark: 0,
                grade:[],
                auto:true,
        },
        schoolform:{
          provinces:[],
          citys:[],
          countys:[],
          schools:[]
        },
        popoverVisible:false,
        questionDetailsVisible:false,
        step1Visible:true,
        step2Visible:false,
        step3Visible:false,
        step4Visible:false,
        formkey1:{
          prop:0,
          schoolTagVisible:false,
          knowledgeTagVisible:false,
          schoolTags:[],
          knowledgeTags:[],
        },
         provinceOptions: [],
         cityOptions: [],
         countyOptions: [],
         schoolOptions: [],
         subjectOptions: subjectOpts,
        KPOptions: [],
        schoolOptionsCas:[],
        KPOptionsCas:[],
        KP:[],
        gradeOptions: gradeOpts,
        qTypeOptions: typeOpts,
        selectedTypes:[],
        data:[],
        qno:[],
        
        };
    },
    methods: {
       handleDragStart(node, ev) {
        console.log('drag start', node);
      },
      handleDragEnter(draggingNode, dropNode, ev) {
        console.log('tree drag enter: ', dropNode.label);
      },
      handleDragLeave(draggingNode, dropNode, ev) {
        console.log('tree drag leave: ', dropNode.label);
      },
      handleDragOver(draggingNode, dropNode, ev) {
        console.log('tree drag over: ', dropNode.label);
      },
      handleDragEnd(draggingNode, dropNode, dropType, ev) {
        console.log('tree drag end: ', dropNode && dropNode.label, dropType);
      },
      handleDrop(draggingNode, dropNode, dropType, ev) {
        console.log('tree drop: ', dropNode.label, dropType);
      },
      allowDrop(draggingNode, dropNode, type) {
        if (dropNode.data.label === '二级 3-1') {

          return (type !== 'inner'&&type !== 'next'&&type !== 'prev');
        } else {
          return false;
        }
      },
      allowDrag(draggingNode) {
        return draggingNode.data.label.indexOf('三级 3-2-2') === -1;
      },
      handlePOptionsChange(data){
        this.cityOptions=[];
        this.countyOptions=[];
        this.schoolOptions=[];
        this.schoolform.citys=[];
        this.schoolform.countys=[];
        this.schoolform.schools=[];
        var reg=/\u5e02$/;
        for(var i in data){
          for(var j in this.provinceOptions){
            if(this.provinceOptions[j].no==data[i]){
              if(reg.test(this.provinceOptions[j].label)){
                var newcity=this.provinceOptions[j];
                this.cityOptions.push(newcity);
              }
              else{
                var c = this.provinceOptions[j].children
                for(var k in c){
                var newcity = c[k]
                this.cityOptions.push(newcity);
                }
              }
              break;
            }
        }
        }
      },
      handleCOptionsChange(data){
        this.countyOptions=[];
        this.schoolOptions=[];
        this.schoolform.countys=[];
        this.schoolform.schools=[];
        for(var i in data){
          for(var j in this.cityOptions){
            if(this.cityOptions[j].no==data[i]){        
                var c = this.cityOptions[j].children
                for(var k in c){
                var newcounty = c[k]
                this.countyOptions.push(newcounty);
                }
              break;
            }
        }
        }
      },
      handleCoOptionsChange(data){
        this.schoolOptions=[];
        this.schoolform.schools=[];
        for(var i in data){
          for(var j in this.countyOptions){
            if(this.countyOptions[j].no==data[i]){ 
              if(this.countyOptions[j].children) {     
                var c = this.countyOptions[j].children
                for(var k in c){
                var newschool = c[k]
                this.schoolOptions.push(newschool);
                }
              }
              break;
            }
        }
        }
      },
      
      
      handlePeriorStep1(){
        this.step1Visible=true;
        this.step2Visible=false;
        this.curstep=1;
        this.data=[];
      },
      handlePeriorStep2(){
        this.step2Visible=true;
        this.step3Visible=false;
        this.curstep=2;
      },
      handlePeriorStep3(){
        this.step3Visible=true;
        this.step4Visible=false;
        this.curstep=3;
      },
      handleQuestionAdjust(){
        var qarr=[];
        var arr=[];
        var length=[];
        for(var i in this.selectedTypes){
          var l = 0;
          length.push(this.selectedTypes[i].qnum);
          var t=this.selectedTypes[i].type;
          for(var j in this.qno){
            for(var k in this.data){
              if(this.data[k].key==this.qno[j]){
                if(this.data[k].type_no==t){
                  arr.push({id:this.qno[j],label:this.data[k].question_content});
                  l++;    
              }  
            } 
            }
          }
          if(l!=length[i]){
            this.$message(
              { message: '题目数出错!',
                type: 'warning'
                });
            return;
          }
        }
        var sum=0;
        for(var i in length){
          
          qarr.push({id:-1,label:Dicts.typeOpts[this.selectedTypes[i].type].label,children:arr.slice(0,1)});
          sum+=length[i];
          alert(arr.slice(sum,sum+length[i]));
        }
        this.qdata=[].concat(qarr);
        
        this.step2Visible=false;
        this.step3Visible=true;
        this.curstep=3;
      },
      handlePaperpreview(){
        this.step3Visible=false;
        this.step4Visible=true;
        this.curstep=4;

      },
      handleQuestionCreate(){
        //检查类型是否有输入不当的地方
        //检查是否有输入不当的地方-5.23
        //生成相应题目数量
        if(this.form1.school===''||this.form1.mark===''||this.form1.grade===''||this.form1.subject===''){
           this.$message(
              { message: '请将基础信息填写完整！',
                type: 'warning'
                });
            return;
        }
        if(typeof(this.form1.mark)!=typeof(1)){
          alert(typeof(this.form1.mark));

          this.$message(
              { message: '总分必须为数字类型!',
                type: 'warning'
                });
            return;
        }
        if(this.form1.mark<=0){
          this.$message(
              { message: '总分必须大于0!',
                type: 'warning'
                });
            return;
        }
        if(this.selectedTypes.length<=0){
          this.$message(
              { message: '必须添加至少一种题型',
                type: 'warning'
                });
            return;
        }
        var sum=0;
        for(var i=0;i<this.selectedTypes.length;i++){
          if(this.selectedTypes[i].type===''||this.selectedTypes[i].qnum===''||this.selectedTypes[i].maxDiffiDegree===''||this.selectedTypes[i].minDiffiDegree===''||this.selectedTypes[i].point===''){
            this.$message(
              { message: '请将题型信息填写完整！',
                type: 'warning'
                });
            return;
          }
          if(this.selectedTypes[i].minDiffiDegree>this.selectedTypes[i].maxDiffiDegree){
            this.$message(
              { message: '难度信息输入错误！',
                type: 'warning'
                });
            return;
          }
          sum+=this.selectedTypes[i].qnum*this.selectedTypes[i].point
        }
        if(sum!=this.form1.mark){
          this.$message(
              { message: '分数信息输入错误！',
                type: 'warning'
                });
                return;
        }

        //生成题目
        //如果form1.auto=true 需要随机选择相应题目放在右边
        //输入对应参数获取题型题干
        this.handlesetting()
        var have=false;
        var st=this.selectedTypes
        var sn=this.formkey1.schoolTags;
        var kpn=[].concat(this.formkey1.knowledgeTags);
        
        for(var a in sn){
          for(var b in kpn){
            for(var i in st){
            
          if(st[i].minDiffiDegree==st[i].maxDiffiDegree){
             this.getQuestionsFromBackend(st[i].minDiffiDegree,st[i].type,Dicts.typeOpts[st[i].type].label,this.form1.subject,sn[a],kpn[b],st[i].point);
          }
          else if(st[i].minDiffiDegree==1&&st[i].maxDiffiDegree==3){
            this.getQuestionsFromBackend(0,st[i].type,Dicts.typeOpts[st[i].type].label,this.form1.subject,sn[a],kpn[b],st[i].point);

          }else{
            this.getQuestionsFromBackend(st[i].minDiffiDegree,st[i].type,Dicts.typeOpts[st[i].type].label,this.form1.subject,sn[a],kpn[b],st[i].point);
            this.getQuestionsFromBackend(st[i].maxDiffiDegree,st[i].type,Dicts.typeOpts[st[i].type].label,this.form1.subject,sn[a],kpn[b],st[i].point);

          }
        }
          }
        }   
        this.step2Visible=true;
        this.step1Visible=false;
        this.curstep=2;

      },
      handlesetting(){
        if(!this.formkey1.schoolTagVisible){
          this.formkey1.schoolTags=[];
          this.formkey1.schoolTags.push(0);
        }
        else if(this.schoolform.schools.length!=0){
          this.formkey1.schoolTags=this.schoolform.schools;

        }else if(this.schoolform.countys.length!=0){
          this.formkey1.schoolTags=this.schoolform.countys;

        }else if(this.schoolform.citys.length!=0){
          this.formkey1.schoolTags=this.schoolform.citys;

        }else{
          this.formkey1.schoolTags=this.schoolform.provinces;
        }
        if(!this.formkey1.knowledgeTagVisible){
          this.formkey1.knowledgeTags=[];
          this.formkey1.knowledgeTags.push(0);
        }

      },
      handleAddQuestionType(){
        var newType={
          type:'',
          id:this.selectedTypes.length,
          qnum:0,
          maxDiffiDegree:3,
          minDiffiDegree:1,
          point:0,
          };
        this.selectedTypes.push(newType);

      },
      removeType(id){
        for(var i=0;i<this.selectedTypes.length;i++){
          if(id==this.selectedTypes[i].id){
            this.selectedTypes.splice(i,1);
            break;
          }
        }
      },
      handleChange(value, direction, movedKeys) {
        
      },
      handleConfirm(){
        this.$emit('childFn', this.qno);
      },
      handleSchoolCas(l,objs){
        var reg1=/\u533a$/;
        var reg2=/\u53bf$/;
        
        for(var i in objs){
          if(!objs[i].children){
            if(reg1.test(objs[i].label)||reg2.test(objs[i].label)){
              objs[i].disabled=true;
            }
          }else{
            if(l==1){
              var newprovince = {no: objs[i].no,label:objs[i].label,value:objs[i].value,children: objs[i].children};
              this.provinceOptions.push(newprovince);
              }
            }
            this.handleSchoolCas(2,objs[i].children);
          }
      },
      handleKPOptionsCas(data){
        
        for(var i in this.KPOptionsCas){
          if(this.form1.subject==this.KPOptionsCas[i].value){
            this.KP=this.KPOptionsCas[i].children;
            break;
          }
        }
        this.formkey1.knowledgeTags=[];
        this.KPOptions=[];
        this.pushKP(this.KP);
      },
      pushKP(KP){
        for(var i in KP){
          if(!KP[i].children){
            var newkp=KP[i];
            this.KPOptions.push(newkp);
          }
          else{
            var newkp={no:KP[i].no,value:KP[i].value,label:KP[i].label};
            this.KPOptions.push(newkp);
            this.pushKP(KP[i].children);
          }
        }
      },
      
      getSchoolsFromBackend(){
        var that = this;
        const path = '/api/get/SourcesNo';
          axios.get(path).then(function (response) {
            var msg = response.data;
            that.schoolOptionsCas=msg;
            that.handleSchoolCas(1,that.schoolOptionsCas);
          }).catch(function (error) {
            alert(error);
          })
      },
      getKPFromBackend(){
        var that = this;
        const path = '/api/get/KnowledgePoints';
          axios.get(path).then(function (response) {
            var msg = response.data;
            that.KPOptionsCas=msg;
          }).catch(function (error) {
            alert(error);
          })
      },
      getQuestionsFromBackend(diff,type_no,type,subject_no,sn,kpn,point){
        
      var conditionForm = {
          keyword: '',
          question_diff: diff,
          question_type: type_no,
          paper_subject: subject_no,
          paper_source: sn,
          paper_grade: [this.gradeOptions[this.form1.grade[0]].children[this.form1.grade[1]-1].no],
          knowledge_point: kpn,
          paper_nature: this.formkey1.prop,
      };
      this.$axios({
        method:'post',
        url:'/api/get/Question',
        data:JSON.stringify({    //这里是发送给后台的数据
            questionOffset: 0,
            questionNum: 1000,
            conditionForm: conditionForm,
          }),
      }).then((response) => {
        var qs=response.data.questions;
        var hs=false;
        for(var i in qs){

           var q = {label:qs[i].question_content,type:type,point:point,key:qs[i].question_no,type_no:type_no}
           for(var j in this.data){
             if(this.data[j].key==q.key){
               hs=true;  
           }}
           if(hs){
             hs=false;

           }else{
             this.data.push(q);
           }
        }
       
      }).catch((error) => {
        alert(error);
      });
    }
    },    
    created(){
      this.getSchoolsFromBackend();
      this.getKPFromBackend();

    }
};
</script>

<style>

 #editor {
        margin: auto;
        width: 90%;
        height: 300px;
    }
  .qinput{
    width:10%;
  }
  .nextButton{
    width: 10%;
    float: none;
    margin-left: auto; 
    margin-right: auto;
    text-align:center;
  }
  
  .box-card {
    width: 90%;
    margin-left: auto; 
    margin-right: auto;
    margin-top: 50px;
    margin-bottom: 50px;
  }

  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  .clearfix:after {
      clear: both
  }
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }
</style>