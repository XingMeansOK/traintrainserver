var express = require('express');
var mysql=require("mysql");
// var query=require("../lib/processData");
var router = express.Router();


/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'home page' });
});

router.get('/query', function(req, res, next) {
    var pool  = mysql.createPool({
        host: 'localhost',
        user: 'root',
        password: '66666666',
        database: 'traintrain',
    });
    pool.query("select * from location", function (error, results, fields) {
        if (error) throw error;
        console.log('The solution is: ', results[0].solution);
    });
});

module.exports = router;
