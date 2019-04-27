'use strict';
// import MdButton from '../node_modules/vue-material/dist/components'
// import 'node_modules/vue-material/dist/vue-material.min.css'
// import axios from 'axios';
// some important global variables.
// the data source
const API_SERVER = 'https://webhose.io/filterWebContent?token=6caf20d8-8bad-49fb-996e-0726d3621783';
const QUERY = '&sort=crawled&q=site_type%3Anews%20thread.country%3AUS%20language%3Aenglish';
const FORMAT = '&format=json';
const COMMENT_VIEW = 'connectsf_comment';
const OUR_API = 'http://ec2-35-167-124-232.us-west-2.compute.amazonaws.com:3000/articles'
// main function
let _featJson;
async function initialPrep() {

  console.log('1...');
  _featJson = await getNews();

  console.log('2... ');
  console.log("data", app_news.news);

  console.log('3... ');


  console.log('4... ');
  // await fetchAddLayers();

  console.log('5... ');
  // await checkCookie();

  console.log('6 !!!');
}
var posts = []

console.log("posts", posts);

// get data from RESTapi
async function getNews() {
  let data_url = API_SERVER + FORMAT + QUERY;
  let resp = await fetch(data_url);

  app_news.news = jsonData['posts'];
}

// var displayed = sample.posts.slice(0,10)
// var news = fetch(api)
// console.log('news', news)
// console.log("")

let app_news = new Vue({
  delimiters:['[[', ']]'], // resolve confilt with jinja2
	el: '#feed',
	data:{
    news: [],
    displayed_news: [],
    filtered_news: [],
    drawer: true,
    time: new Date(),
    my_articles: [],
    topics: ['Politics', 'Sports', 'Business', 'Current Events'],
    topic_on: [false, false, false, false],
    clicked_ids: new Set(),
    input_email: '',
    input_pwd: '',
    page_length: 0,
    page: 1,
    first_idx: 0,
    last_idx: 10
	},

	computed: {
	},

  //Used to grab data from rest-api
  mounted:function(){
      axios.get(OUR_API)
        .then(function (response) {
          console.log("data", response.data)
          app_news.news = response.data
          app_news.displayed_news = response.data.slice(0,10)
          app_news.page_length = Math.ceil(response.data.length/10)
        })
  },

	methods:{

		renderArticle: function(idx){
			var clicked = this.displayed_news[idx]
      var click_id = this.my_articles.length
      clicked['click_id'] = click_id

      if( !this.clicked_ids.has(clicked.article_id) ){
        this.my_articles.push(clicked)
        this.clicked_ids.add(clicked.article_id)
      }
      console.log("my articles", this.my_articles)
		},
    handleSignUp: function(idx) {
      console.log(this.input_email + ' ' + this.input_pwd);
      axios.post('http://127.0.0.1:5000/register', {
        password: this.input_pwd,
        email: this.input_email
      })
      .then(function (response) {
        console.log(response);
      });
    },
    handleLogIn: function(idx) {
      console.log(this.input_email + ' ' + this.input_pwd);
      axios.post('http://127.0.0.1:5000/login', {
        password: this.input_pwd,
        email: this.input_email
      })
      .then(function (response) {
        console.log(response);
      });
    },
    removeArticle: function(index, clicked){
      if (this.my_articles.length == 1){
        this.my_articles = []
        this.clicked_ids = new Set()
      }else{
        this.my_articles.splice(index, index+1)
        this.clicked_ids.delete(clicked.article_id)
      }
    },
    chooseTopic: function(index){
      console.log('topics', this.topics)
      this.topic_on[index] = !this.topic_on[index]
    },
    nextPage: function(page){
      // Using incremements of 10, extract the start/end index articles 
      this.first_idx = (page - 1)*10
      if (this.news.length < page*10){
        this.last_idx = this.news.length
      }else{
        this.last_idx = page*10
      }
      this.displayed_news = this.news.slice(this.first_idx, this.last_idx)
    }

	}
})

// initialPrep()
console.log('hello')
console.log('sample', sample.posts)
