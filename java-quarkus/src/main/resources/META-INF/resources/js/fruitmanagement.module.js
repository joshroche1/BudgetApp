var app = angular.module("FruitManagement", []);

//Controller Part
app.controller("FruitManagementController", function ($scope, $http) {

//Initialize page with default data which is blank in this example
$scope.fruits = [];

$scope.form = {
  id: -1,
  name: ""
};

//Now load the data from server
_refreshPageData();

//HTTP POST/PUT methods for add/edit fruits
$scope.update = function () {
  var method = "";
  var url = "";
  var data = {};
  if ($scope.form.id == -1) {
    //Id is absent so add fruits - POST operation
    method = "POST";
    url = '/fruits';
    data.name = $scope.form.name;
    data.category = $scope.form.category;
    data.notes = $scope.form.notes;
  } else {
    //If Id is present, it's edit operation - PUT operation
    method = "PUT";
    url = '/fruits/' + $scope.form.id;
    data.name = $scope.form.name;
    data.category = $scope.form.category;
    data.notes = $scope.form.notes;
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

//HTTP DELETE- delete fruit by id
$scope.remove = function (fruit) {
  $http({
    method: 'DELETE',
      url: '/fruits/' + fruit.id
    }).then(_success, _error);
  };

  //In case of edit fruits, populate form with fruit data
  $scope.edit = function (fruit) {
    $scope.form.name = fruit.name;
    $scope.form.category = fruit.category;
    $scope.form.notes = fruit.notes;
    $scope.form.id = fruit.id;
  };

  /* Private Methods */
  //HTTP GET- get all fruits collection
  function _refreshPageData() {
    $http({
      method: 'GET',
      url: '/fruits'
    }).then(function successCallback(response) {
      $scope.fruits = response.data;
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
    $scope.form.category = "";
    $scope.form.notes = "";
    $scope.form.id = -1;
  }
});
