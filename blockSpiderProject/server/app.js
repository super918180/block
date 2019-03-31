'use strict'
//引入express
const express = require("express")
//解析前端传过来的数据的中间件
const bodyParse = require("body-parser")
//初始化express
const app = express()
//引入controller
var $ = require('./controller/controller.js');

var model = require('../mongodb/model.js')
const localPort = 3000
const jsonParser = bodyParse.json()

app.set('view engine', 'html');
//解决通信跨域的问题
app.use(function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS');
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header('Access-Control-Allow-Headers', 'Content-Type');
    res.header("Content-Type", "application/json; charset=utf-8")
    next();
})

app.get('/', $.list)
app.get('/search', $.list)
app.get('/display', $.list)
app.get('/createKeyWords',$.createKeyWords);
app.get('/getKeyWords',$.listKeyWords)
app.get('/deleteArticle',$.deleteArticle)
app.listen(localPort, () => {
    console.log('http://127.0.0.1:%s', localPort)
})