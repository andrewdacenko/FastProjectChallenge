# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Topic'
        db.create_table(u'main_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tu', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 9, 0, 0))),
        ))
        db.send_create_signal(u'main', ['Topic'])

        # Adding model 'Comment'
        db.create_table(u'main_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cu', to=orm['auth.User'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='ct', to=orm['main.Topic'])),
            ('q_comment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cc', to=orm['main.Topic'])),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_add', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 9, 0, 0))),
        ))
        db.send_create_signal(u'main', ['Comment'])

        # Adding model 'TopicUserLike'
        db.create_table(u'main_topicuserlike', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tulu', to=orm['auth.User'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tult', to=orm['main.Topic'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['TopicUserLike'])

        # Adding model 'CommentUserLike'
        db.create_table(u'main_commentuserlike', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='culu', to=orm['auth.User'])),
            ('comment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='culc', to=orm['main.Comment'])),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'main', ['CommentUserLike'])

        # Adding model 'Vote'
        db.create_table(u'main_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vuf', to=orm['auth.User'])),
            ('user_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vut', to=orm['auth.User'])),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(related_name='vt', to=orm['main.Topic'])),
        ))
        db.send_create_signal(u'main', ['Vote'])


    def backwards(self, orm):
        # Deleting model 'Topic'
        db.delete_table(u'main_topic')

        # Deleting model 'Comment'
        db.delete_table(u'main_comment')

        # Deleting model 'TopicUserLike'
        db.delete_table(u'main_topicuserlike')

        # Deleting model 'CommentUserLike'
        db.delete_table(u'main_commentuserlike')

        # Deleting model 'Vote'
        db.delete_table(u'main_vote')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'main.comment': {
            'Meta': {'object_name': 'Comment'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 9, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'q_comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cc'", 'to': u"orm['main.Topic']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ct'", 'to': u"orm['main.Topic']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cu'", 'to': u"orm['auth.User']"})
        },
        u'main.commentuserlike': {
            'Meta': {'object_name': 'CommentUserLike'},
            'comment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'culc'", 'to': u"orm['main.Comment']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'culu'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'main.topic': {
            'Meta': {'object_name': 'Topic'},
            'date_add': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 9, 9, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tu'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'main.topicuserlike': {
            'Meta': {'object_name': 'TopicUserLike'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tult'", 'to': u"orm['main.Topic']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tulu'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'main.vote': {
            'Meta': {'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vt'", 'to': u"orm['main.Topic']"}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vuf'", 'to': u"orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'vut'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['main']