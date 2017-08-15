var mysql=require("mysql");
const TYPES = ['once', 'twice', 'thrice'];
var pool  = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '66666666',
    database: 'traintrain',
});
// pool.query("select * from location", function (error, results, fields) {
//     if (error) throw error;
//     console.log('The solution is: ', results[0].solution);
// });

pool.getConnection(function(err, connection) {
    // Use the connection
    connection.query("select * from location", function (error, results, fields) {
        // And done with the connection.
        connection.release();

        // Handle error after the release.
        if (error) throw error;

        // Don't use the connection here, it has been returned to the pool.
    });
});
/*
*  加工数据的方法，将算法得到的数据（火车站点）添加上坐标信息
* */
const processData = function(dataObject) {
    TYPES.forEach(function(type) {
        dataObject[type].forEach(function(plan) {

        })
    })
}
module.exports=query;