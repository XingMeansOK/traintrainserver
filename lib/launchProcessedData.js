var exec = require('child_process').exec;
var mysql=require("mysql");
var fs=require('fs');
const CMDPREFIX = 'py -3 D:\\workspace\\traintrainserver\\lib\\trainTransfer.py';
const CLASSIFYTYPES = ['nonstop', 'once', 'twice'];

/*
* mysql连接池
* */
var pool  = mysql.createPool({
    host: 'localhost',
    user: 'root',
    password: '66666666',
    database: 'traintrain',
});

/**
 * 对算法的计算结果进行加工
 * @result object 算法的原始结果
 * @res response 用来向前端发送数据的对象，由post或者get函数提供
 * */
function processResultThenLaunch(result, res) {
    var index = 0;// 为每种方案添加上唯一的编号
    var promiseArr = [];
    CLASSIFYTYPES.forEach( type => {
        // 遍历每一种方案
        result[type].forEach( plan => {
            plan.selected = false;
            plan.index = index++;
            // stations中的元素还是数组，一个数组代表一个车次，车次内的元素是对象，代表途径的车站
            plan.stations.forEach(train => {
                // 遍历每一个车站
                train.forEach(station => {
                    // Use the connection
                    var queryStr = "select * from location where `﻿name` like '"+ station.name+"%'";

                    let promise = new Promise((resolve, reject) => {
                        pool.getConnection(function(err, connection) {
                            connection.query(queryStr, function (error, results, fields) {
                                station.x = results[0].latitude;
                                station.y = results[0].longitude;
                                // query是异步的，当异步结果成功返回了之后，改变当前promise的状态
                                if(station.x){
                                    resolve();// resolve里面可以放个啥将来给then用，但是这里不需要了
                                }
                                // And done with the connection.
                                connection.release();

                                // Handle error after the release.
                                if (error) throw error;

                                // Don't use the connection here, it has been returned to the pool.
                            });
                        });
                    });
                    // 将所有的promise保存起来
                    promiseArr.push(promise);
                })
            })
        })
    });
    // 当所有的promise都resolve之后，也就是说所有的查询都执行成功了，将加工好的数据发送给前端
    Promise.all(promiseArr).then(() => {
        res.json(result);
    })

}

/**
 * 调用python算法，获取其计算结果，并对结果进行加工，给所有的站点都加上坐标信息
 * 前四个参数是查询算法需要的参数
 * @start string 出发站
 * @destination string 终点站
 * @t1 number 相同车站换乘最大时间间隔
 * @t2 number 市内换乘最大时间间隔
 * @res response 用来向前端发送数据的对象，由post或者get函数提供
 * */
function launchProcessedData(start, destination, t1, t2, res) {
    const cmd = `${CMDPREFIX} ${start} ${destination} ${t1} ${t2}`;

    /**
     * 产生一个子进程用于处理cmd命令行，也就是说就相当于在命令行中执行字符串cmd
     * 第二个参数function ：called with the output when process terminates
     * 当子进程结束的时候会调用这个回调函数
     * 还是很智能的，虽然是用回调函数处理异步，不过能有就不错了。这里调用的脚本会将结果写入result.json中
     * 写完了子进程才算结束
     * */
    exec(cmd,function(error,stdout,stderr){
        // 如果出错就直接返回了
        if(error) {
            console.info('stderr : '+stderr);
            return;
        }
        console.info('done');
        // 获取计算结果的原始值
        // 先去掉require模块的缓存 这种方法不可行啊，缓存去不掉
        // delete require.cache['../public/json/result.json'];
        // let result = require('../public/json/result.json');
        let file = "D:\\workspace\\traintrainserver\\public\\json\\result.json";
        let result=JSON.parse(fs.readFileSync(file));
        processResultThenLaunch(result, res);
    });
}
module.exports = launchProcessedData;