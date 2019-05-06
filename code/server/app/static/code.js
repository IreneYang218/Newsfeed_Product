'use strict';
// import MdButton from '../node_modules/vue-material/dist/components'
// import 'node_modules/vue-material/dist/vue-material.min.css'
// import axios from 'axios';
// some important global variables.
// the data source
const OUR_API = 'http://ec2-35-167-124-232.us-west-2.compute.amazonaws.com:3000/articles'

function updateChart() {
  let chart = document.getElementById("chart");
  if (!chart) return;

  let trips = Math.round(
    tripTotals[chosenTaz][day]['pickups'] + tripTotals[chosenTaz][day]['dropoffs'] );
  let title = buildPopupTitle(trips);

  let element = document.getElementById("popup-title");
  element.innerHTML = title;

  // fetch the details
  let finalUrl = api_server + 'tnc_trip_stats?taz=eq.' + chosenTaz
                            + '&day_of_week=eq.' + day

  fetch(finalUrl).then((resp) => resp.json()).then(function(jsonData) {
      let data = buildChartDataFromJson(jsonData);
      if (currentChart) currentChart.setData(data);
  }).catch(function(error) {
      console.log("err: "+error);
  });
}

let app_news = new Vue({
  delimiters:['[[', ']]'], // resolve confilt with jinja2
	el: '#feed',
	data:{
    news: [],
    displayed_news: [],
    filtered_news: [],
    politics_news: [],
    sports_news: [],
    business_news: [],
    current_news: [],
    drawer: true,
    time: new Date(),
    my_articles: [],
    topics: ['Politics', 'Sports', 'Business', 'Current Events'],
    topic_on: [false, false, false, false],
    chosen_topics: new Set(),
    clicked_ids: new Set(),
    input_email: '',
    input_pwd: '',
    logged_in: false,
    logged_in_user: '',
    page_length: 0,
    page: 1,
    first_idx: 0,
    last_idx: 10
	},

	computed: {
	},

  //Used to grab data from rest-api
  mounted:function(){
      // axios.get('/userinfo')
      //   .then(response => {
      //     console.log(response);
      //     this.logged_in = true;
      //     this.logged_in_user = response.data.email;
      //   })
      //   .catch(error => {
      //     console.log(error);
      //   });
      axios.get(OUR_API)
        .then(function (response) {
          console.log("data", response.data)
          app_news.news = response.data
          app_news.filtered_news = response.data
          app_news.displayed_news = response.data.slice(0,10)
          app_news.page_length = Math.ceil(response.data.length/10)

          // Hardcoding the general topic
          app_news.news.forEach(function(article){
            var rand_int = Math.floor(Math.random() * (+4 - +0)) + +0
            article.general_topic = app_news.topics[rand_int]
          })
          app_news.news.forEach(function(article){
            var topic = article.general_topic
            if(topic=='Politics'){
              app_news.politics_news.push(article)
            }else if(topic=='Sports'){
              app_news.sports_news.push(article)
            }else if(topic=='Business'){
              app_news.business_news.push(article)
            }else{
              app_news.current_news.push(article)
            }
          })
        })
        .catch(error => {
          console.log(error);
        });
      axios.get(OUR_API+"?select=news_topic")
        .then(function (response)) {
          console.log("topic", response.data);
        }
        .catch(error => {
          console.log(error);
        });
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
      console.log("my articles", this.my_articles);
      updateChart();
		},
    handleSignUp: function(idx) {
      console.log(this.input_email + ' ' + this.input_pwd);
      axios.post('/register', {
        password: this.input_pwd,
        email: this.input_email
      })
      .then(function (response) {
        console.log(response);
      });
    },
    handleLogIn: function(idx) {
      console.log(this.input_email + ' ' + this.input_pwd);
      axios.post('/login', {
        password: this.input_pwd,
        email: this.input_email
      })
      .then(response => {
        if (response.data.status === 'ok') {
          this.logged_in_user = response.data.user;
          this.logged_in = true;
          console.log(this.logged_in);
        }
      })
      .catch(error => {
        console.log(error);
      })
    },
    handleLogOut: function(idx) {
      axios.post('/logout')
      .then(response => {
        if (response.data.status === 'ok') {
          this.logged_in_user = '';
          this.logged_in = false;
          console.log(this.logged_in);
        }
      })
      .catch(error => {
        console.log(error);
      })
    },
    removeArticle: function(index, clicked){
      console.log("index", index)
      if (this.my_articles.length == 1){
        this.my_articles = []
        this.clicked_ids = new Set()
      }else{

        this.my_articles.splice(index, 1)
        this.clicked_ids.delete(clicked.article_id)
      }
    },
    chooseTopic: function(topic){
      if(this.chosen_topics.has(topic)){
          this.chosen_topics.delete(topic)
      }else{
        this.chosen_topics.add(topic)
      }
      if(this.chosen_topics.size == 0){
        this.filtered_news = this.news
      }else{
        this.filtered_news = []
        if(this.chosen_topics.has('Politics')){
          this.filtered_news = this.filtered_news.concat(this.politics_news)
        }
        if(this.chosen_topics.has('Sports')){
          this.filtered_news = this.filtered_news.concat(this.sports_news)
        }
        if(this.chosen_topics.has('Business')){
          this.filtered_news = this.filtered_news.concat(this.business_news)
        }
        if(this.chosen_topics.has('Current')){
          this.filtered_news = this.filtered_news.concat(this.current_news)
        }
      }
      if(this.filtered_news.length <= 10){
        this.displayed_news = this.filtered_news
        this.page_length = 1
      }else{
        this.displayed_news = this.filtered_news.slice(0,10)
        this.page_length = Math.ceil(this.filtered_news.length/10)
      }
      updateChart();
    },
    nextPage: function(page){
      // Using incremements of 10, extract the start/end index articles
      this.first_idx = (page - 1)*10
      if (this.filtered_news.length < page*10){
        this.last_idx = this.filtered_news.length
      }else{
        this.last_idx = page*10
      }
      this.displayed_news = this.filtered_news.slice(this.first_idx, this.last_idx)
    },
	}
})
