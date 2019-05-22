<template>
<div>
  <el-collapse v-model="activeNames">
  <el-collapse-item  name="1">
    <template slot="title">
      <span>编辑辅助</span>
    </template>
  <el-button type="primary" class="button" size="mini" @click.prevent="insertInputTxt(' \\')">换行符</el-button>
  <el-button type="primary" class="button" size="mini" @click.prevent="insertInputTxt('$$')">插入公式</el-button>
  <el-button class="button" size="mini" @click.prevent="insertInputTxt('\\____')">插入下划线</el-button>

  <el-popover
    placement="top"
    title="希腊字母"
    width="210"
    trigger="hover">
    <el-button class="button"  size="mini" v-for="text,name in alphabets" circle :key="name" :class="'iconfont icon-icon-'+ text" @click.prevent="insertInputTxt('\\'+text)"></el-button>
    <el-button class="button" slot="reference" size="mini">希腊字母</el-button>
  </el-popover>
    <el-popover
    placement="top"
    title="常用符号"
    width="210"
    trigger="hover">
    <el-button class="button" v-for="text, name in ops" circle @click.prevent="insertInputTxt(text)" :key="name"></el-button>
    <el-button class="button" slot="reference" size="mini">常用符号</el-button>
  </el-popover>
    <el-popover
    placement="top"
    title="其他"
    width="210"
    trigger="hover">
    <el-button class="button" v-for="text, name in ops" circle @click.prevent="insertInputTxt(op)" :key="name"></el-button>
    <el-button class="button" slot="reference" size="mini">其他</el-button>
  </el-popover>
  </el-collapse-item>
  <el-collapse-item title="Markdown编辑器" name="2">
    <mavon-editor 
    v-model="curContent"
    :toolbars="toolbars"
    :boxShadow="false"
    ref="md"
    @imgAdd="$imgAdd" @imgDel="$imgDel"
    />
  </el-collapse-item>
  </el-collapse>
  <el-button type="primary" class="button" @click.prevent="saveContent" size="medium">保存</el-button>

</div>


</template>

<script>

export default {
  name: 'Editor',
  props: ['content'],
  data () {
    return {
          img_file:[],
          editorOptions:{
            modules:{
              toolbar:[
                ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
                ['blockquote', 'code-block'],
                ['formula']
              ]
            }
          },
          curContent: this.content,
          alphabets:[
            'alpha','beta','gamma','delta',
            'epsilon','zeta','eta','theta',
            'iota','kappa','lambda','mu',
            'nu','xi','omicron','pi','rho',
            'sigma','tau','upsilon','phi',
            'chi','omega'
          ],
          ops:{
            'prod0': '\\prod',
            'prod1': '\\prod_{}^{}',
            'sum0': '\\sum',
            'sum1': '\\sum_{}^{}',
            'sqrt0': '\\sqrt{}',
            'sqrt1': '\\sqtr[]{}',
            'bigcap0': '\\bigcap',
            'bigcup0': '\\bigcup',
            'int0': '\\int',
            'int1': '\\int_{}^{}',
            'lim0':'\\lim_{}',
            'frac0':'\\frac{}{}',
            'frac1':'{}\\tfrac{}{}',
            'leftbrace':'\\{',
            'rightbrace':'\\}',
            'les':'<',
            'gtr': '>',
            'leq': '\\leq',
            'geq': '\\geq',
            'neq': '\\neq',
            'to': '\\to',
          },

          formula: '$中间为公式内容$',
          activeNames:['1','2'],
          toolbars: {
            bold: true, // 粗体
            italic: true, // 斜体
            header: true, // 标题
            underline: false, // 下划线
            mark: false, // 标记
            superscript: false, // 上角标
            quote: false, // 引用
            ol: true, // 有序列表
            link: true, // 链接
            code: true, // code
            subfield: true, // 是否需要分栏
            fullscreen: true, // 全屏编辑
            readmodel: true, // 沉浸式阅读
            /* 1.3.5 */
            undo: true, // 上一步
            trash: true, // 清空
            // save: true, // 保存（触发events中的save事件）
            /* 1.4.2 */
            navigation: true, // 导航目录
            imagelink: true
          }

    }
  },
  methods:{
    insertInputTxt(insertTxt) {
      let elInput = this.$refs.md.$refs.vNoteTextarea.$refs.vTextarea;
      let startPos = elInput.selectionStart;
      let endPos = elInput.selectionEnd;
      if (startPos === undefined || endPos === undefined) return
      let txt = elInput.value;
      let result = txt.substring(0, startPos) + insertTxt + txt.substring(endPos)
      elInput.value = result;
      elInput.focus();
      if (insertTxt == '$$'){
        elInput.selectionStart = startPos + insertTxt.length-1;
        elInput.selectionEnd = startPos + insertTxt.length-1;
      }
      else{
        elInput.selectionStart = startPos + insertTxt.length;
        elInput.selectionEnd = startPos + insertTxt.length;
      }
      this.curContent = result;
    },
    saveContent(){
      this.$emit('new', this.curContent);
    },
    $imgAdd(pos, $file) {
    // 第一步.将图片上传到服务器.
      var formdata = new FormData();
      formdata.append('figure', $file);
      this.img_file[pos] = $file;
      this.$axios({
          url: '/uploadFig',
          method: 'post',
          data: formdata,
          headers: { 'Content-Type': 'multipart/form-data' },
      }).then((res) => {
          let _res = res.data;
          // 第二步.将返回的url替换到文本原位置![...](0) -> ![...](url)
          this.$refs.md.$img2Url(pos, _res.url);
      }).catch((error) => {
          console.log(error);
      })
    },
    $imgDel(pos) {
      delete this.img_file[pos];
    }
  },
  watch: {
    content: {
      immediate: true,
      handler(content) {
        this.curContent = content;
      }
    }
  }
}
</script>
<style scoped>
.button {
  margin-bottom: 1%;
  margin-top: 1%;
  margin-left: 0px;
}

</style>
