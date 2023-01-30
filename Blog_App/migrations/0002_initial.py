# Generated by Django 4.0.5 on 2022-11-21 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Blog_App', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='postvotesmodel',
            name='vote_post_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_post_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='post_tag',
            field=models.ManyToManyField(related_name='post_tag', to='Blog_App.tagsmodel'),
        ),
        migrations.AddField(
            model_name='postsmodel',
            name='post_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_post', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentvotesmodel',
            name='vote_com_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_com_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='commentvotesmodel',
            name='vote_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vote_comment', to='Blog_App.commentsmodel'),
        ),
        migrations.AddField(
            model_name='commentsmodel',
            name='com_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='com_post', to='Blog_App.postsmodel'),
        ),
        migrations.AddField(
            model_name='commentsmodel',
            name='com_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL),
        ),
    ]