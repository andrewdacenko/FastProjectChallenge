if (Topics.find().count() === 0) {
	Topics.insert({
		title: 'Introducing Telescope',
		author: 'Sacha Greif',
	});

	Topics.insert({
		title: 'Meteor',
		author: 'Tom Coleman',
	});

	Topics.insert({
		title: 'The Meteor Book',
		author: 'Tom Coleman',
	});
}

Meteor.publish('topics');