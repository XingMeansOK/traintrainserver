var express = require('express');
var mysql=require("mysql");
var launchProcessedData=require("../lib/launchProcessedData");
var router = express.Router();


/* GET home page. */
router.get('/', function(req, res, next) {
    res.render('index', { title: 'home page' });
});

router.post('/query', function(req, res, next) {
    const { start, destination, t1, t2 } = req.body;
    launchProcessedData(start, destination, Number(t1), Number(t2), res);
});

module.exports = router;
