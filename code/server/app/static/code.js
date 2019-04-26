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
const api = 'http://ec2-35-167-124-232.us-west-2.compute.amazonaws.com:3000/articles'
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

// get data from RESTapi
async function getNews() {
  let data_url = API_SERVER + FORMAT + QUERY;
  let resp = await fetch(data_url);

  app_news.news = jsonData['posts'];
}

var news = fetch(api)
console.log('news', news)

// const colors = ["indigo","blue","cyan","light-blue","teal","light-green","blue-grey"];
let app_news = new Vue({
  delimiters:['[[', ']]'], // resolve confilt with jinja2
	el: '#feed',
	data:{
    news: sample.posts,
    drawer: true,
    time: new Date(),
    my_articles: [],
    topics: ['topic a', 'topic b', 'topic c', 'topic d'],
    topic_on: [false, false, false, false], 
    clicked_ids: new Set(),
    input_email: '',
    input_pwd: ''
	},

	computed: {
	},

	methods:{

		renderArticle: function(idx){
			var clicked = sample.posts[idx]
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
    }
	}
})



// initialPrep()
console.log('hello')
console.log('sample', sample.posts)
