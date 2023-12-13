# Generated by Django 4.2.7 on 2023-12-11 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_remove_postcomment_mentioned_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='post_images',
        ),
        migrations.AddField(
            model_name='post',
            name='post_media',
            field=models.FileField(blank=True, null=True, upload_to='post_media/'),
        ),
        migrations.AddField(
            model_name='post',
            name='post_type',
            field=models.CharField(choices=[('text', 'text'), ('video', 'video'), ('audio', 'audio'), ('images', 'images')], default='text', max_length=50),
        ),
    ]