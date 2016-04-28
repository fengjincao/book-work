/**
 * Created by developer on 16-4-25.
 */
(function(window, angular, undefined) {
    'use strict';
    var book_houseApp = angular.module('book_house', ['ipCookie']);
    book_houseApp.controller('book_houseCtrl', ['$scope','$window','$http','ipCookie', function($scope,$window,$http,ipCookie) {
        $scope.user_name = "";
        $scope.limitnumber= 2;
        $scope.show_detail=false;
        $scope.show_modify=false;
        $scope.show_add=false;
        $scope.next_disable = false;
        $scope.books = [];
        $scope.token = {};
        $scope.before_id = 0;
        $scope.showDetail = {
            'book_id':'',
            'book_name':'',
            'book_price':'',
            'book_intro':'',
            'owner_name':''
        };
        $scope.addDetail= {
            'book_name':'',
            'book_price':'',
            'book_intro':''
        };
        $scope.modifyDetail= {
            'book_id':'',
            'book_name':'',
            'book_price':'',
            'book_intro':''
        };
        $scope.init_page = function(){
            $scope.user_name = ipCookie('name');
            $scope.token = {'token': ipCookie('token')};
            $scope.getMyBooks();
        };
        $scope.sign_out = function(){
            ipCookie.remove('token',{path:'/'});
            ipCookie.remove('name',{path:'/'});
            $window.location.href="/";
        };
        $scope.next_page = function(){
            $scope.before_id = $scope.books[$scope.books.length - 1].book_id;
            $scope.getMyBooks();

        };
        $scope.getMyBooks = function(){
            $http({
                headers: $scope.token,
                method:'GET',
                url:'/api/books/',
                params: {'before_id': $scope.before_id},
            }).success(function(data, status, headers, config){
                var content = data['data'];
                if (data['status'] === 'success') {
                    $scope.books = $scope.books.concat(content['books']);
                    $scope.next_disable = content['next_disable'];
                }
                else if (data['status'] === 'fail') {
                    alert("error occur");
                }
            }).error(function(data, status, headers, config){

            });
        };
        $scope.detailDialog = function(book_id){
            $http({
                headers: $scope.token,
                method: 'GET',
                url: '/api/books/'+ book_id.toString() +'/',
            }).success(function(data){
                $scope.showDetail= data['book'];
                $scope.show_detail = true;
            });
        };
        $scope.modifyDialog = function(book_id){
            $http({
                headers: $scope.token,
                method: 'GET',
                url: '/api/books/'+ book_id.toString() +'/',
            }).success(function(data){
                $scope.modifyDetail= data['book'];
                $scope.show_modify= true;
            });
        };
        $scope.book_modify = function(){
            $http({
                headers: $scope.token,
                method: 'PUT',
                url: '/api/books/' + $scope.modifyDetail['book_id'].toString() + '/',
                data: $scope.modifyDetail
            }).success(function(){
                $scope.getMyBooks();
                $scope.show_modify= false;
            });
        }
        $scope.book_delete = function(book_id){
             $http({
                headers: $scope.token,
                method: 'DELETE',
                url: '/api/books/'+ book_id.toString() +'/',
            }).success(function(data, status, headers, config) {
                 $scope.getMyBooks();
             });
        };
        $scope.book_add = function(){
            $http({
                headers: $scope.token,
                method: 'POST',
                url: '/api/books/',
                data: $scope.addDetail

            }).success(function(){
                $scope.getMyBooks();
                $scope.show_add= false;
            });
        };
    }]);


})(window, window.angular);
