≧<template>
<div>
  <el-collapse v-model="activeNames">
  <el-collapse-item name="0" title="帮助">
    <span>Markdown是一种可以使用普通文本编辑器编写的标记语言，通过简单的标记语法，它可以使普通文本内容具有一定的格式。
    该编辑器正是基于Markdown这一标记语言，左边为输入框，右边为预览处。<br>
    在[编辑辅助]中提供了各种选项，可以帮助您编辑文本。如需插入公式请先点击[插入公式], 再填写公式内容，部分特殊字符编码需在公式中才可使用(公式中请避免使用空格，公式两边请加空格，暂不支持中文)。<br>
    初次使用可根据案例和预览处结果稍作尝试 :)<br>
    例: <br>
    复制以下公式至下方编辑器可看到结果，所出现的符号在辅助选项中均有提供。<br>
    分子分母: ${x^2}\tfrac{y_1}{2}$ <br>
    双氧水分解: $H_20_2\xrightarrow[\Delta]{Mn0_2}H_20+0_2\uparrow$<br>
    </span>
  </el-collapse-item>
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
    <el-button class="button" slot="reference" size="mini">常用希腊字母</el-button>
  </el-popover>
    <el-popover
    placement="top"
    title="常用符号"
    width="600"
    trigger="hover">
    <el-button class="button" v-for="text, name in ops"  :class="'iconfont icon-'+ name"  @click.prevent="insertInputTxt(text)" :key="name"></el-button>
    <el-button class="button" slot="reference" size="mini">常用符号</el-button>

  </el-popover>
    <el-popover
    placement="top"
    title="其他"
    width="220"
    trigger="hover">
    <el-button class="button chemical" v-for="text, name in chemicalOps" :class="'iconfont icon-'+ name" @click.prevent="insertInputTxt(text)" :key="name"></el-button>
    <el-button class="button" slot="reference" size="mini">化学公式</el-button>
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
            'epsilon','eta','theta',
            'kappa','lambda','miu','xi','pi','rho',
            'sigma','tau','phi',
            'chi','omega','Alpha','Beta','Delta','Gamma','Lambda','Omega','Phi','Pi','Psi','Sigma','Theta'
          ],
          ops:{
            'subscript':'_{}',
            'superscript':'^{}',
            'div':'\\div',
            'times':'\\times',
            'cong':'\\cong',
            'sim' :'\\sim',
            'in': '\\in',
            'notin':'\\notin',
            'because':'\\because',
            'therefore':'\\therefore',
            'emptyset':'\\emptyset',
            'vec':'\\vec{}',
            'prod': '\\prod',
            'prod1': '\\prod_{}^{}',
            'sum': '\\sum',
            'sum1': '\\sum_{}^{}',
            'sqrt': '\\sqrt{}',
            'sqrt1': '\\sqrt[]{}',
            'cap': '\\cap',
            'cup': '\\cup',
            'frac':'\\frac{}{}',
            'frac1':'{}\\tfrac{}{}',
            'leftbrace':'\\{',
            'rightbrace':'\\}',
            'les':'<',
            'grt': '>',
            'leq': '\\leq',
            'geq': '\\geq',
            'neq': '\\neq',
            'approx':'\\approx',
            'pm':'\\pm',
            'circ': '^{\\circ}',
            'degf':'^{\\circ}F',
            'degc':'^{\\circ}C',
            'wedge':'\\wedge',
            'vee':'\\vee',
            'Rightarrow':'\\Rightarrow',
            'Leftarrow':'\\Leftarrow',
            'Leftrightarrow':'\\Leftrightarrow'
          },
          chemicalOps:{
            'rightarrow':'\\rightarrow',
            'rightarrow1':'\\overset{}{\\rightarrow}',
            'rightarrow2':'\\xrightarrow[]{}',
            'rightleftharpoons':'\\rightleftharpoons',
            'Delta':'\\Delta',
            'uparrow':'\\uparrow',
            'downarrow':'\\downarrow'
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
  margin-right: 0px;
  margin-left: 0px;
}
.chemical{
    width: 110px;
}
</style>
