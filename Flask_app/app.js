
var app = angular.module("app", ['ngTable', 'ngRoute']);

// Router
app.config(function($routeProvider) {
    console.log($routeProvider)
    $routeProvider
    .when("/", {
        templateUrl : "views/main.html"
    })
    .otherwise({
        templateUrl : "views/main.html"
    });
});

// Controllers
app.controller("MainController", ['$scope','$http','$location', function ($scope,$http,$location) {
    var path= 'http://localhost:5000/';
    var data;
    $http.get(path)
        .then(function(response){
            data=response.data.data;
            console.log(data)
            $scope.roles = data
        },function(response){
            console.log("Error")
        })
}]);