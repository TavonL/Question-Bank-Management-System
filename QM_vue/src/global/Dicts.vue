<script>
    const subjectOpts= [{
            value: 0,
            label: '不限'
        },{
            value: 1,
            label: '语文'
        },{
            value: 2,
            label: '数学'
        },{
            value: 3,
            label: '英语'
        },{
            value: 4,
            label: '物理'
        }, {
            value: 5,
            label: '化学'
        },{
            value: 6,
            label: '生物'
        },{
            value: 7,
            label: '地理',
        },{
            value: 8,
            label: '历史',
        },{
            value: 9,
            label: '政治'
        }];
    const gradeOpts = [{
        value: 0,
        label: '不限',
        no: [1,2,3,4,5,6,7,8,9,10,11,12]
    },{
        value: 1,
        label: '小学',
        no: [1,2,3,4,5],
        children: [{
            value: 1,
            label:'小学一年级',
            no: 1,
        },{
            value: 2,
            label:'小学二年级',
            no: 2,
        },{
            value: 3,
            label:'小学三年级',
            no: 3,
        },{
            value: 4,
            label:'小学四年级',
            no: 4,
        },{
            value: 5,
            label:'小学五年级',
            no: 5,
        }]
    },{
        value: 2,
        label: '初中',
        no: [6,7,8,9],
        children: [{
            value: 1,
            label: '预备',
            no: 6,
        },{
            value: 2,
            label:'初中一年级',
            no: 7,
        },{
            value:3,
            label:'初中二年级',
            no: 8,
        },{
            value:4,
            label:'初中三年级',
            no:9,
        }]
    },{
        value: 3,
        label: '高中',
        no: [10, 11, 12],
        children: [{
            value: 1,
            label:'高中一年级',
            no: 10,
        },{
            value: 2,
            label: '高中二年级',
            no: 11
        },{
            value: 3,
            label: '高中三年级',
            no: 12,
        }]
    }];
    const typeOpts = [{
        value: 0,
        label: '不限'
    },{
        value: 1,
        label: '填空题'
    },{
        value: 2,
        label: '单选题'
    },{
        value: 3,
        label: '多选题' 
    },{
        value: 4,
        label: '应用题'
    },{
        value: 5,
        label: '综合题'
    }];
    const diffOpts = [{
        value: 0,
        label: '不限',
    },{
        value: 1,
        label: '简单' 
    },{
        value: 2,
        label: '中等',
    },{
        value: 3,
        label: '难'
    }];
    const propertyOpts = [{
        value: 0,
        label: '不限',
    },{
        value: 1,
        label: '公办(公立)' 
    },{
        value: 2,
        label: '民办(私立)',
    }];

    function outputObj(obj) {
	var description = "";
	for (var i in obj) {
		description += i + " = " + obj[i] + "\n";
	}
	alert(description);
    }

    export default
    {
        subjectOpts,
        gradeOpts,
        typeOpts,
        diffOpts,
        propertyOpts,
        outputObj,

    }
</script>