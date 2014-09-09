/* globals angular */
'use strict';

(function() {

	function IndexController($scope) {
		var now = new Date();
		var data = [{
			title: 'First',
		}, {
			title: 'Second',
		}, {
			title: 'Third',
		}];

		[2, 5, 10].forEach(function(minute, index) {
			now.setMinutes(now.getMinutes() - minute);
			var time = now;
			console.log('time', time);
			data[index].date_add = (time).toISOString();
		});

		console.log(data);

		$scope.active = angular.copy(data);
		$scope.voting = angular.copy(data);
		$scope.archive = angular.copy(data);

		$scope.pageLoadTime = (new Date()).toISOString();
		// $scope.nowTime = nowTime;
	};

	angular
		.module('MyApp', ['angularMoment'])
		.config(function($interpolateProvider) {
			$interpolateProvider.startSymbol('{$');
			$interpolateProvider.endSymbol('$}');
		})
		.controller('IndexController', ['$scope', IndexController]);

})();