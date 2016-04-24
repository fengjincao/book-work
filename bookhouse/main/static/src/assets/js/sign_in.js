(function(window, angular, undefined) {
    'use strict';
    var signInApp = angular.module('signIn', ['ipCookie']);
    signInApp.controller('signInCtrl', ['$scope','$window','$http','ipCookie', function($scope,$window,$http,ipCookie) {
        $scope.name = "";
        $scope.password = "";
        $scope.signIn_submit=function(){
        $http({
                method: 'POST',
                url: '/api/account/sign-in/',
                data: {
                    'name': $scope.name,
                    'password': $scope.password
                }
              }).success(function (data, status, headers, config) {
                var content = data['data'];
                if(data['status']==='success') {
                  ipCookie('name', content['name'], {path: '/', expires: 90});
                  ipCookie('gender', content['gender'], {path: '/', expires: 90});
                  ipCookie('token', content['token'], {path: '/', expires: 90});
                  $window.location='/index'
                }
                else if (data['status']==='fail') {
                  alert((content['code']));
                }
              }).error(function(data, status, headers, config) {

              });
        };
        $scope.signUp=function(){
            $window.location.href='/account/sign-up/'
        };
    }]);


})(window, window.angular);
