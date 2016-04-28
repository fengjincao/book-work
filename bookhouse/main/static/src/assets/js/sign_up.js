(function(window, angular, undefined) {
    'use strict';
    var signUpApp = angular.module('signUp', ['ipCookie']);
    signUpApp.controller('signUpCtrl', ['$scope','$window','$http','ipCookie', function($scope,$window,$http,ipCookie) {
        $scope.GENDER_OPTIONS = [
            {
                'name': '男',
                'magic': 1
            },
            {
                'name': '女',
                'magic': 2
            }
        ];
        $scope.name = "";
          $scope.password = "";
          $scope.gender = null;
          $scope.signup_submit=function(){
            $http({
                    method: 'POST',
                    url: '/api/account/sign-up/',
                    data: {
                        'name': $scope.name,
                        'password': $scope.password,
                        'gender' : $scope.gender
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

    }]);

})(window, window.angular);
