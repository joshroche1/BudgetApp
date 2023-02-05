var app = angular.module("UserManagement", []);

//Controller Part
app.controller("UserManagementController", function ($scope, $http) {

//Initialize page with default data which is blank in this example
$scope.users = [];

$scope.form = {
  id: -1,
  name: ""
};

//Now load the data from server
_refreshPageData();

//HTTP POST/PUT methods for add/edit users
$scope.update = function () {
  var method = "";
  var url = "";
  var data = {};
  if ($scope.form.id == -1) {
    //Id is absent so add users - POST operation
    method = "POST";
    url = '/users';
    data.name = $scope.form.name;
    data.email = $scope.form.email;
  } else {
    //If Id is present, it's edit operation - PUT operation
    method = "PUT";
    url = '/users/' + $scope.form.id;
    data.name = $scope.form.name;
    data.email = $scope.form.email;
  }

  $http({
    method: method,
    url: url,
    data: angular.toJson(data),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(_success, _error);
};

//User Login
$scope.userlogin = function () {
  var method = "POST";
  var url = "/users/login";
  var data = {};
  data.name = $scope.form.name;
  data.password = $scope.form.password;

  $http({
    method: method,
    url: url,
    data: angular.toJson(data),
    headers: {
      'Content-Type': 'application/json'
    }
  }).then(_success, _error);
};

//HTTP DELETE- delete user by id
$scope.remove = function (user) {
  $http({
    method: 'DELETE',
      url: '/users/' + user.id
    }).then(_success, _error);
  };

  //In case of edit fruits, populate form with fruit data
  $scope.edit = function (user) {
    $scope.form.name = user.name;
    $scope.form.email = user.email;
    $scope.form.id = user.id;
  };

  /* Private Methods */
  //HTTP GET- get all fruits collection
  function _refreshPageData() {
    $http({
      method: 'GET',
      url: '/users'
    }).then(function successCallback(response) {
      $scope.users = response.data;
    }, function errorCallback(response) {
      console.log(response.statusText);
    });
  }

  function _success(response) {
    _refreshPageData();
    _clearForm()
  }

  function _error(response) {
    alert(response.data.message || response.statusText);
  }

  //Clear the form
  function _clearForm() {
    $scope.form.name = "";
    $scope.form.email = "";
    $scope.form.id = -1;
  }
});
