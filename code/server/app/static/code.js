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

function compare(a, b) {
  // Helper function to sort descending
  // Use toUpperCase() to ignore character casing
  const countA = a.count;
  const countB = b.count;

  let comparison = 0
  if (countA > countB) {
    comparison = -1;
  } else if (countA < countB) {
    comparison = 1;
  }
  return comparison;
}

function countTopics(articles){
  var countDict = {}
  articles.forEach(function(article){
    if(article.news_topic in countDict){
      countDict[article.news_topic] += 1
    }else{
    countDict[article.news_topic] = 1
    }
  })
  return countDict;
}

function getTopicsInfo(articles){
  var countDict = countTopics(articles)
  var keys = Object.keys(countDict)
  var countList = []
  for(var i=0; i < keys.length; i++){
    countList.push({topic: keys[i],
                    count: countDict[keys[i]],
                    avg_score: getMeanControversy(keys[i], articles)})
  }
  return countList.sort(compare)
}

function getMeanControversy(topic, articles){
  console.log("currtop", topic)
  var filtered = articles.filter(article => article.news_topic == topic)
  var total = 0
  for(var i=0; i < filtered.length; i++) {
    total += filtered[i].controversy_score
  }
  return total/filtered.length
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
    topics: ['Politics', 'Sports', 'Business', 'Current Event'],
    topic_info: [],
    topic0: null,
    topic1: null,
    topic2: null,
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
      axios.get(OUR_API+'?limit=1000')
        .then(function (response) {
          console.log("data", response.data)
          app_news.news = response.data
          app_news.filtered_news = response.data
          app_news.displayed_news = response.data.slice(0,10)
          app_news.page_length = Math.ceil(response.data.length/10)
          app_news.topic_info = getTopicsInfo(response.data).slice(0,3)
          app_news.topic0 = app_news.topic_info[0]
          app_news.topic1 = app_news.topic_info[1]
          app_news.topic2 = app_news.topic_info[2]


          // Creating general topic sublists
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
      axios.get(OUR_API+"?news_topic=news_topic")
        .then(function (response) {
          console.log("topic", response.data);
        })
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
        if(this.chosen_topics.has('Current Event')){
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
      this.topic_info = getTopicsInfo(this.filtered_news).slice(0,3)
      this.topic0 = this.topic_info[0]
      this.topic1 = this.topic_info[1]
      this.topic2 = this.topic_info[2]

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
