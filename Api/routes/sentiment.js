var express = require('express');
var request = require('request');
var router = express.Router();

router.get('/', function(req, res, next) {
    txt = req.query.text;
    request('https://api.havenondemand.com/1/api/sync/analyzesentiment/v1?text='+txt+'&apikey=e1e36193-7f28-4d45-86a7-838ee79431ca',
    function(error, response, body) {
        if (!error && response.statusCode == 200) {
            
            res.send(body);

        }
    })

});
    

module.exports = router;