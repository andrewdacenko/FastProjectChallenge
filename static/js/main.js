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
		this.to = null;

		this.submit = function() {
			$http.post('/api/topic/' + self.id, {
				text: this.text
			}).then(function(response) {
				self.text = '';
				self.to = null;
				self.topic = response.data;
			}, function(reason) {
				console.log(reason);
			});
		};

		this.comment = function($event, a) {
			$event.preventDefault();

			this.to = a.user;
			this.text = a.user.username + ', ';

			var form = angular.element('.comment-area');

			form.focus();
		};

		$http.get('/api/topic/' + self.id).then(function(response) {
			self.topic = angular.copy(response.data);
		});
	};

	function NewTopicController($http, $location, $timeout) {
		var self = this;

		this.error = {
			timeout: null,
			text: ''
		};

		this.text = '';

		this.submit = function() {
			if (self.error.timeout) {
				$timeout.cancel(self.error.timeout);
			};

			console.log(self.text.trim().length);

			if ((self.text.trim()).length < 10) {
				self.error.text = 'Need at least 10 symbols';
				self.error.timeout = $timeout(function() {
					self.error.text = '';
				}, 1500);

				return;
			};

			$http
				.post('/api/topics', {
					title: this.text
				})
				.then(function(response) {
					var id = response.data.id;
					window.location = '/topic/' + id;
				}, function(reason) {
					if (reason.status === 401) {
						window.location = '/login';
					};

					self.error.text = 'Something went wrong';
					self.error.timeout = $timeout(function() {
						self.error.text = '';
						self.error.timeout = null;
					}, 1500);
				});
		};
	};

	angular
		.module('MyApp', ['angularMoment', 'ngCookies'])
		.config(function($httpProvider, $interpolateProvider) {
			$interpolateProvider.startSymbol('{$');
			$interpolateProvider.endSymbol('$}');
			$httpProvider.defaults.transformRequest = function(data) {
				if (data === undefined) return data;
				return $.param(data);
			};
			$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
		})
		.controller('IndexController', ['$http', IndexController])
		.controller('StateController', ['$http', '$location', StateController])
		.controller('TopicController', ['$http', '$location', TopicController])
		.controller('NewTopicController', ['$http', '$location', '$timeout', NewTopicController])
		.run(function($http, $cookies) {
			$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
		})

})();