var blockchain = require('./blockSchema.js'); //引入Schema 文件

// var article_catalog = db.collection('article_catalog')
//数据插入
function insert(coll, conditions, callback) {
    conditions = conditions || {};
    blockchain.coll.create(conditions, callback)
}

//数据查询
function find(coll, conditions, callback) {
    conditions = conditions || {};
    if ('article_catalog' == coll) {
        // var model = blockchain.coll
        blockchain.article_catalog.find(conditions, callback).limit(5);
    }

}

//数据更新
function update(coll, conditions, update) {
    blockchain.coll.update(conditions, update, function (err, res) {
        if (err) console.log('Error' + err);
        else console.log('Res:' + res);
    })
}

//数据删除
function del(coll, conditions) {
    blockchain.coll.remove(conditions, function (err, res) {
        if (err) console.log('Error' + err);
        else console.log('Res:' + res);
    })
}

module.exports = {
    find: find,
    del: del,
    update: update,
    insert: insert
};