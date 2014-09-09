/* globals angular */
'use strict';

(function() {

	function IndexController($http) {
		var self = this;

		this.active = [];
		this.voting = [];
		this.archive = [];

		$http.get('/api')
			.then(function(response) {
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

	function TopicController($http, $location, $timeout) {
		var self = this;

		this.id = $location.absUrl().split('/')[4];

		this.topic = {
			comments: []
		};

		this.top = [];
		this.user_choice = null;
		this.topic_votes_sum = 0;

		this.error = {
			timeout: null,
			text: ''
		};

		this.text = '';
		this.to = null;

		this.isLikable = function() {
			var added = (new Date(self.topic.date_add)).getTime();
			var now = new Date();
			now.setDate(now.getDate() - 1);
			return added > now.getTime();
		};

		this.isVotable = function() {
			var added = (new Date(self.topic.date_add)).getTime();
			var oneDay = new Date();
			var twoDays = new Date();
			oneDay.setDate(oneDay.getDate() - 1);
			twoDays.setDate(twoDays.getDate() - 2);
			return added > twoDays.getTime() && added < oneDay.getTime();
		};

		this.submit = function() {
			if (self.error.timeout) {
				$timeout.cancel(self.error.timeout);
			};

			if ((self.text.trim()).length < 1) {
				self.error.text = 'Need at least 1 charachter';
				self.error.timeout = $timeout(function() {
					self.error.text = '';
				}, 1500);

				return;
			};

			var data = {};
			data.text = self.text;

			if (self.to) {
				data.q_comment = self.to.id;
			};

			$http
				.post('/api/topic/' + self.id, data)
				.then(function(response) {
					self.text = '';
					self.to = null;
					self.topic = response.data;
					self.error.text = '';
				}, function(reason) {
					if (reason.status === 401) {
						// window.location = '/login';
					};

					self.error.text = 'Something went wrong';
					self.error.timeout = $timeout(function() {
						self.error.text = '';
						self.error.timeout = null;
					}, 1500);
				});
		};

		this.comment = function($event, a) {
			$event.preventDefault();

			this.to = a.user;
			this.text = a.user.username + ', ';

			var form = angular.element('.comment-area');

			form.focus();
		};

		this.likeTopic = function(bool) {
			var url = !!bool ? 'like' : 'dislike';

			$http
				.post('/api/topic/' + self.id + '/' + url)
				.then(function(response) {
					self.topic.sum = self.topic.sum + (!!bool ? 1 : -1);
				}, function(reason) {
					console.log(reason);
				});
		};

		this.likeComment = function(comment, bool) {
			var url = !!bool ? 'like' : 'dislike';

			$http
				.post('/api/comment/' + comment.id + '/' + url)
				.then(function(response) {
					comment.sum = comment.sum + (!!bool ? 1 : -1);
				}, function(reason) {
					console.log(reason);
				});
		};

		this.vote = function(user) {
			$http
				.post('/api/topic/' + self.id + '/vote', {
					user_id: user.id
				})
				.then(function(response) {
					console.log(response);
				}, function(reason) {
					console.log(reason);
				});
		};

		this.calcVotes = function(user) {
			return ((user.votes / self.topic_votes_sum) * 100).toFixed(1);
		};

		$http.get('/api/topic/' + self.id).then(function(response) {
			self.topic = angular.copy(response.data);
		});

		$http.get('/api/topic/' + self.id + '/top').then(function(response) {
			self.top = angular.copy(response.data.top_users);
			self.user_choice = angular.copy(response.data.user_choice);
			response.data.top_users.forEach(function(item) {
				self.topic_votes_sum += item.votes;
			});
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

	function ProfileController($http, $location) {
		var self = this;

		this.id = $location.absUrl().split('/')[4];

		this.navigateTo = function(comment) {
			window.location = '/topic/' + comment.topic.id;
		};

		$http
			.get('/api/user/' + self.id)
			.then(function(response) {
				self.user = angular.copy(response.data);
			}, function(reason) {
				console.log(reason);
			});
	};

	function ngEnter() {
		return function(scope, element, attrs) {
			element.bind("keydown keypress", function(event) {
				if (event.which === 13 && (event.ctrlKey || event.shiftKey)) {
					scope.$apply(function() {
						scope.$eval(attrs.ngEnter);
					});

					event.preventDefault();
				}
			});
		};
	};

	function appCongif($httpProvider, $interpolateProvider) {
		$interpolateProvider.startSymbol('{$');
		$interpolateProvider.endSymbol('$}');
		$httpProvider.defaults.transformRequest = function(data) {
			if (data === undefined) return data;
			return $.param(data);
		};
		$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded; charset=UTF-8';
	};

	function appRun($http, $cookies) {
		$http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
	};

	angular
		.module('MyApp', ['angularMoment', 'ngCookies', 'ui.bootstrap'])
		.config(['$httpProvider', '$interpolateProvider', appCongif])
		.directive('ngEnter', ngEnter)
		.controller('IndexController', ['$http', IndexController])
		.controller('StateController', ['$http', '$location', StateController])
		.controller('ProfileController', ['$http', '$location', ProfileController])
		.controller('TopicController', ['$http', '$location', '$timeout', TopicController])
		.controller('NewTopicController', ['$http', '$location', '$timeout', NewTopicController])
		.run(['$http', '$cookies', appRun])

})();