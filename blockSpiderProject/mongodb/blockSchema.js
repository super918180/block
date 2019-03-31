var mongoose = require('./dbconfig.js'), // 引入mongodb配置文件
    Schema = mongoose.Schema;

// 构造Schema
var article_catalog_Schema = new Schema({
    title: String, //文章标题
    introduce: String, //文章简介
    artUrl: String, //文章源地址
    sourceUrl: String, //文章来源
    artTime: String, //文章发表时间
});
var article_catalog = mongoose.model('article_catalog', article_catalog_Schema)

var article_body_Schema = new Schema({
    title: String,
    introduce: String,
    body: String,
})
var article_body = mongoose.model('article_body', article_body_Schema)

var article_img_Schema = new Schema({
    title: String,
    img: [{
        imgUrl: String,
        img: String
    }]
})
var article_img = mongoose.model('article_img', article_img_Schema)

var keywordSchema = new Schema({
    keywords: [{
        keywords: String,
        num:String
    }]
})
var  keyword=mongoose.model('keyword',keywordSchema)

module.exports = {
    article_catalog: article_catalog,
    article_body: article_body,
    article_img: article_img,
    keyword:keyword
}