var mysql = require('mysql');

var connection = mysql.createConnection({
  host     : 'localhost',
  user     : 'root',
  password : 'Laiwt0223',
  database : 'qm',
  port:'3306'
});
var sql='SELECT * FROM user';

connection.connect(function(err){
    if(err){
      console.log('---:'+err);
      return;
    }
    console.log('succeed');
});
var sqlData=[];
connection.query(sql,function (err, result) {
        if(err){
          console.log('[SELECT ERROR] - ',err.message);
          return;
        }
 
       console.log('--------------------------SELECT----------------------------');
       for(var i=0;i<result.length;i++)
       {
         sqlData.push({
          userName: result[i].user_name,
          password: result[i].user_pwd,
          permission: result[i].user_auth,
          infoChangeSeen: false,
          changeButton: "modify",
          id:i
         });
       }
       console.log(sqlData);
       console.log('------------------------------------------------------------\n\n');  
});
connection.end(function(err){
  if(err){
    console.log('---:'+err);
    return;
  }
  console.log('succeed');
});