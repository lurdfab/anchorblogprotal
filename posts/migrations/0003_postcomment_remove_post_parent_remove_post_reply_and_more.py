# Generated by Django 4.2.7 on 2023-12-06 17:09

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_post_parent_post_reply'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_comment', models.TextField(max_length=3000)),
                ('is_removed', models.BooleanField(default=False, help_text='Check this box if the comment is inappropriate. A "This comment has been removed" message will be displayed instead.')),
                ('is_nesting_permitted', models.BooleanField(default=False)),
                ('flair', models.TextField(blank=True, max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('mentioned_users', models.ManyToManyField(blank=True, related_name='%(class)s_mentions', to=settings.AUTH_USER_MODEL, verbose_name='mentioned_users')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.postcomment')),
            ],
            options={
                'verbose_name': 'Post Comment',
                'verbose_name_plural': 'Post Comments',
                'ordering': ['created_at'],
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='post',
            name='reply',
        ),
        migrations.CreateModel(
            name='PostCommentVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1), django.core.validators.MaxValueValidator(1)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('post_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='posts.postcomment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Post Comment Vote',
                'verbose_name_plural': 'Post Comment Votes',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddField(
            model_name='postcomment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post', verbose_name='post'),
        ),
        migrations.AddField(
            model_name='postcomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(class)s_comments', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
