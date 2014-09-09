Router.configure({
    layoutTemplate: 'layout',
    loadingTemplate: 'loading',
    waitOn: function() {
        return Meteor.subscribe('topics');
    }
});
Router.map(function() {
    this.route('topicsList', {
        path: '/'
    });
});