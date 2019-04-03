$(document).ready(function () {
    var vue = new Vue({
        el: '#app',
        data() {
            return {
                a: [],
                searchVal: '',
                article_catalog: [],
                //请求类型，1：文章列表，2：文章内容
                searchType: 1,
                page: 0,
                size: 10,
                total: 0,
                currentPage: 1,
                activeIndex: '1',
                activeIndex2: '1',
                keyWords: '',
                showTable: 1,
                createTime: '',
                searchStartTime: '',
                searchEndTime: '',
                type:'',
            }

        },
        mounted() {
            this.searchQuery(1)
        },
        methods: {
            search: function () {
                this.searchQuery(1);
            },
            searchQuery: function (page) {
                var self = this;
                //使用axios进行请求
                axios.get('http://localhost:3000/search?type=' + self.type + '&articleTitle=' + self.searchVal + '&startTime=' + self.searchStartTime + '&endTime=' + self.searchEndTime + '&page=' + (page ? page : 0) + '&size=' + self.size).then(function (res) {
                    self.article_catalog = res.data.content;
                    self.total = res.data.totalElements;
                })
            },
            search: function (e) {
                // console.log(e)
                this.searchQuery(1)
            },
            pageChange: function (e) {
                this.searchQuery(e)
            },
            handleClick: function (e) {
                window.open(e.artUrl, target = '_blank')
            },
            changeTable: function (showType) {
                this.showTable = showType;
            },
            createKeyWords: function () {
                var self=this;
                axios.get("http://localhost:3000/createKeyWords").then(function (res) {
                    console.log(res);
                    if(res.data=='success'){
                        self.getKeyWords();
                    }
                })
            },
            handleSelect(key, keyPath) {
                console.log(key, keyPath);
            },
            getKeyWords: function () {
                this.changeTable(4);
                var self = this;
                axios.get("http://localhost:3000/getKeyWords").then(function (res) {
                    self.createTime = res.data.content[0].createTime;
                    self.keyWords = res.data.content[0].keywords[0];
                    self.total = Object.keys(self.keyWords).length
                    console.log(self.createTime)
                })
            },
            handleDelete: function (e) {
                var artTitle = e.title
                axios.get('http://localhost:3000/deleteArticle?artTitle=' + artTitle).then(function (res) {
                    console.log(res)
                })
                this.searchQuery(1)
            },
            searchLatestNews:function(){
               this.searchVal='';
               this.searchStartTime='';
               this.searchEndTime='';
                this.changeTable(1);
                this.type='recommend';
                this.searchQuery(1);
            },
            searchPolicyNews:function(){
                this.searchVal='';
                this.searchStartTime='';
                this.searchEndTime='';
                this.changeTable(1);
                this.type='policy';
                this.searchQuery(1);
            },
            searchOtherNews:function(){
                this.searchVal='';
                this.type='';
                this.searchStartTime='';
                this.searchEndTime='';
                this.changeTable(1);
                this.searchQuery(1);
            }

        },


    })
});