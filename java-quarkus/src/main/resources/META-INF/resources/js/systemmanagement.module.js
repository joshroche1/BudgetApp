var app = angular.module("SystemManagement", []);

//Controller Part
app.controller("SystemManagementController", function ($scope, $http) {

//Initialize page with default data which is blank in this example
$scope.systems = [];

$scope.form = {
  id: -1,
  hostname: ""
  ipaddress: ""
  category: ""
  group: ""
  os: ""
  notes: ""
};

//Now load the data from server
_refreshPageData();

//HTTP POST/PUT methods for add/edit system
$scope.update = function () {
  var method = "";
  var url = "";
  var data = {};
  if ($scope.form.id == -1) {
    //Id is absent so add system - POST operation
    method = "POST";
    url = '/systems';
    data.hostname = $scope.form.hostname;
    data.ipaddress = $scope.form.ipaddress;
    data.category = $scope.form.category;
    data.groups = $scope.form.group;
    data.os = $scope.form.os;
    data.notes = $scope.form.notes;
  } else {
    //If Id is present, it's edit operation - PUT operation
    method = "PUT";
    url = '/systems/' + $scope.form.id;
    data.hostname = $scope.form.hostname;
    data.ipaddress = $scope.form.ipaddress;
    data.category = $scope.form.category;
    data.groups = $scope.form.group;
    data.os = $scope.form.os;
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

//HTTP DELETE- delete system by id
$scope.remove = function (system) {
  $http({
    method: 'DELETE',
      url: '/systems/' + system.id
    }).then(_success, _error);
  };

  //In case of edit systems, populate form with system data
  $scope.edit = function (system) {
    $scope.form.hostname = system.hostname;
    $scope.form.ipaddress = system.ipaddress;
    $scope.form.id = system.id;
  };

  /* Private Methods */
  //HTTP GET- get all systems collection
  function _refreshPageData() {
    $http({
      method: 'GET',
      url: '/systems'
    }).then(function successCallback(response) {
      $scope.systems = response.data;
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
    $scope.form.hostname = "";
    $scope.form.ipaddress = "";
    $scope.form.category = "";
    $scope.form.group = "";
    $scope.form.os = "";
    $scope.form.notes = "";
    $scope.form.id = -1;
  }
});
