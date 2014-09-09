/* globals angular */
'use strict';

(function() {

	function IndexController($http) {
		var self = this;

		this.active = [];
		this.voting = [];
		this.archive = [];

		$http.get('/api').then(function(response) {
			self.active = angular.copy(response.data.active);
			self.voting = angular.copy(response.data.voting);
			self.archive = angular.copy(response.data.archive);
		});
	};

	function StateController($http, $location) {
		var self = this;

		this.topics = [];
		this.title = '';

		var type = $location.absUrl().split('/')[3];

		var types = ['active', 'voting', 'archive'];

		if (types.indexOf(type) !== -1) {

			this.title = type.charAt(0).toUpperCase() + type.slice(1);

			$http.get('/api/' + type).then(function(response) {
				self.topics = angular.copy(response.data);
			});

		};
	};

	function TopicController($http, $location) {
		var self = this;

		this.id = $location.absUrl().split('/')[4];

		this.topic = {
			comments: []
		};

		this.text = '';

		this.comment = function() {
			$http.post('/api/topic/' + self.id, {
				text: this.text
			}).then(function(response) {
				self.topic.comments.push(response.data);
			}, function(reason) {
				console.log(reason);
			});
		}


		$http.get('/api/topic/' + self.id).then(function(response) {
			self.topic = angular.copy(response.data);
		});
	};

	angular
		.module('MyApp', ['angularMoment'])
		.config(function($interpolateProvider) {
			$interpolateProvider.startSymbol('{$');
			$interpolateProvider.endSymbol('$}');
		})
		.controller('IndexController', ['$http', IndexController])
		.controller('StateController', ['$http', '$location', StateController])
		.controller('TopicController', ['$http', '$location', TopicController])

})();