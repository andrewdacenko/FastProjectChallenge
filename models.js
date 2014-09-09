// declare collections
// this code should be included in both the client and the server
Topics = new Meteor.Collection("topics");
Comments = new Meteor.Collection("comments");
Votes = new Meteor.Collection("votes");

CommentLikes = new Meteor.Collection('comment_likes');
TopicLikes = new Meteor.Collection('topic_likes');
VoteLikes = new Meteor.Collection('vote_likes');