'use strict';
// import MdButton from '../node_modules/vue-material/dist/components'
// import 'node_modules/vue-material/dist/vue-material.min.css'

// some important global variables.
// the data source
const API_SERVER = 'https://webhose.io/filterWebContent?token=6caf20d8-8bad-49fb-996e-0726d3621783';
const QUERY = '&sort=crawled&q=site_type%3Anews%20thread.country%3AUS%20language%3Aenglish';
const FORMAT = '&format=json';
const COMMENT_VIEW = 'connectsf_comment';

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
    clicked_links: new Set(),
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

      if( !this.clicked_links.has(clicked.url) ){
        this.my_articles.push(clicked)
        this.clicked_links.add(clicked.url)
      }
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
        this.clicked_links = new Set()
      }else{
        this.my_articles.splice(index, index+1)
        this.clicked_links.delete(clicked.url)
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
