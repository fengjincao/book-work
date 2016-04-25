/**
 * Created by developer on 16-4-25.
 */
(function(window, angular, undefined) {
    'use strict';
    var book_houseApp = angular.module('book_house', ['ipCookie']);
    book_houseApp.controller('book_houseCtrl', ['$scope','$window','$http','ipCookie', function($scope,$window,$http,ipCookie) {
        $scope.user_name = "";
        $scope.books = [];
        $scope.init_page = function(){
            $scope.user_name = ipCookie('name');
            $scope.getMyBooks();
        };
        $scope.sign_out = function(){
            ipCookie.remove('token');
            ipCookie.remove('name');
            ipCookie.remove('gender');
            $window.location.href="/";
        };
        $scope.getMyBooks = function(){
            $http({
                headers: {'token': ipCookie('token')},
                method:'GET',
                url:'/api/books/'
            }).success(function(data, status, headers, config){
                var content = data['data'];
                if(data['status']==='success')
                    $scope.books = content['books'];
                else if(data['status']==='fail'){
                    alert("error occur");
                }
            }).error(function(data, status, headers, config){

            });
        };
    }]);


})(window, window.angular);
