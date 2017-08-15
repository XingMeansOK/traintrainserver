var express = require('express');
var router = express.Router();

/* GET users listing. */
// 这个就测试用了，现在没用了
router.post('/', function(req, res, next) {
  // res.send('respond with a resource');
    const plan = {
        type1: [
            {x:123.38333,y:41.80000},
            {x:104.06667,y:30.66667}
        ],
        type2: [
            {x:114.31667,y:30.51667},
            {x:114.48333,y:38.03333}
        ],
        type3: [
            {x:120.33333,y:36.06667},
            {x:115.90000,y:28.68333}
        ],
    }


    res.json(plan);
});

module.exports = router;
