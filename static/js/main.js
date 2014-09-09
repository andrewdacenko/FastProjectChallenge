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

	function nl2br($sce) {
		return function(msg, is_xhtml) {
			var is_xhtml = is_xhtml || true;
			var breakTag = (is_xhtml) ? '<br />' : '<br>';
			var msg = (msg + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
			return $sce.trustAsHtml(msg);
		}
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
	// .filter('nl2br', ['$sce', nl2br])
	.controller('IndexController', ['$http', IndexController])
		.controller('StateController', ['$http', '$location', StateController])
		.controller('TopicController', ['$http', '$location', TopicController])
		.run(function($http, $cookies) {
			$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
		})

})();