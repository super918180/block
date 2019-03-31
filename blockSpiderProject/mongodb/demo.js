var service = require('./model.js')


var conditions = {
    'title': "两会中，关于区块链的声音"
}
var list = service.find('article_catalog', conditions, function (err, doc) {
    if (err) {
        res.end(err);
        return
    }
    //这里直接返回数据库返回的数据，我并没有进行其他封装，所以返回的是一个数组，后续会考虑统一标准
    // res.end(JSON.stringify(doc));
    console.log(doc)
});