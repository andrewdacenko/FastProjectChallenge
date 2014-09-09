// Meteor.publish("activeTopics", function() {
// 	var now = new Date();
// 	var yesterday = new Date();
// 	yesterday.setDate(now.getDate() - 1);
// 	return Topics.find({}, {
// 		dateAdd: {
// 			$gte: yesterday
// 		}
// 	});
// });

// Meteor.publish("voteTopics", function() {
// 	var now = new Date();
// 	var yesterday = new Date();
// 	var beforeYesterday = new Date();
// 	yesterday.setDate(now.getDate() - 1);
// 	beforeYesterday.setDate(now.getDate() - 1);
// 	return Topics.find({}, {
// 		dateAdd: {
// 			$lte: yesterday,
// 			$gte: beforeYesterday
// 		}
// 	});
// });

// Meteor.publish("archiveTopics", function() {
// 	var now = new Date();
// 	var beforeYesterday = new Date();
// 	beforeYesterday.setDate(now.getDate() - 2);
// 	return Topics.find({}, {
// 		dateAdd: {
// 			$lte: beforeYesterday
// 		}
// 	});
// });

Meteor.publish('topics');