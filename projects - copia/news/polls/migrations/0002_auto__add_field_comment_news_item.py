# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field comments on 'News'
        db.delete_table('polls_news_comments')

        # Adding field 'Comment.news_item'
        db.add_column(u'polls_comment', 'news_item',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=3, to=orm['polls.News']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding M2M table for field comments on 'News'
        db.create_table(u'polls_news_comments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('news', models.ForeignKey(orm[u'polls.news'], null=False)),
            ('comment', models.ForeignKey(orm[u'polls.comment'], null=False))
        ))
        db.create_unique(u'polls_news_comments', ['news_id', 'comment_id'])

        # Deleting field 'Comment.news_item'
        db.delete_column(u'polls_comment', 'news_item_id')


    models = {
        u'polls.comment': {
            'Meta': {'object_name': 'Comment'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.News']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.User']"})
        },
        u'polls.news': {
            'Meta': {'object_name': 'News'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['polls.User']"})
        },
        u'polls.user': {
            'Meta': {'object_name': 'User'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['polls']