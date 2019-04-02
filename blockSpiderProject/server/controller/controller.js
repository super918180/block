var model = require('../../mongodb/model.js'); // 引入model文件
var blockchain = require('../../mongodb/blockSchema.js'); //引入Schema 文件
var utils = require('./utils.js');
var keyExec = require('child_process').exec
//获取文章列表

list = function (req, res, next) {
        //从请求中取出来的数据都是字符串
        //解析get请求所携带的参数articleTitle
        var title = req.query.articleTitle;
        var startTime = req.query.startTime;
        var endTime = req.query.endTime;
        if (startTime == '' || startTime == 'null') {
            startTime = '1970'
        }
        if (endTime == '' || endTime == 'null') {
            endTime = '3000'
        } else {
            endTime = utils.formatUnixtimestamp(endTime)
            console.log(endTime)
        }

        var type = req.query.type;
        //解析get请求所携带的参数searchType
        //解析page
        var page = req.query.page;
        //解析 get 请求中所携带的参数 size
        var size = req.query.size;
        console.log(size)
        var coll = 'article_catalog'
        //
        blockchain[coll].find({
            "title": {
                $regex: title,
                $options: '$i'
            },
            'type': {
                $regex: type,
            },
            'artTime': {
                $gte: startTime,
                $lte: endTime
            },
        }, function (err, ress) {
            if (err) {
                res.end(err)
            }
            console.log(ress);
            var totalElements = ress.length;
            blockchain[coll].find({
                "title": {
                    $regex: title,
                    $options: '$i'
                },
                'type': {
                    $regex: type,
                },
                'artTime': {
                    $gte: startTime,
                    $lte: endTime
                }

            }, {
                //0表示返回不显示此字段，1表示显示此字段
                '_id': 0,
            }).limit(parseInt(size)).
            skip(parseInt(page - 1) * 5).exec(function (err, doc) {
                if (err) {
                    res.end(err)
                }
                console.log(doc)
                res.send({
                    'content': doc,
                    'totalElements': totalElements,
                    'size': size,
                    'numberOfElements': doc.length

                })
            })

        })

    },
    listKeyWords = function (req, res, next) {
        // var key = req.query.keyword;
        blockchain['keyword'].find({}, {
            '_id': 0,
        }).sort({
            createTime: -1
        }).limit(1).exec(function (err, doc) {
            if (err) {
                res.end(err)
            }
            res.send({
                'content': doc,
            })
        })


    },
    createKeyWords = function (req, res) {
        keyExec('python   D:\\VueProject\\blockSpiderProject-master\\server\\controller\\createKeyWords.py', function (error, stdout, stderr) {
            if (error) {
                console.log("error", error)
            } else {
                console.log('stdout: ', stdout);
                res.send('success')
            }
        });
    },
    deleteArticle = function (req, res) {
        var title = req.query.artTitle;
        blockchain.article_catalog.deleteOne({
            'title': title
        }).exec(function (err, doc) {
            if (err) {
                res.end(err)
            }
        });
        blockchain.article_body.deleteOne({
            'title': title
        }).exec(function (err, doc) {
            if (err) {
                res.end(err)
            }
        });
        blockchain.article_img.deleteOne({
            'title': title
        }).exec(function (err, doc) {
            if (err) {
                res.end(err)
            }
            res.send('success')
        });


    }


module.exports = {
    list: list,
    createKeyWords: createKeyWords,
    listKeyWords: listKeyWords,
    deleteArticle: deleteArticle
};