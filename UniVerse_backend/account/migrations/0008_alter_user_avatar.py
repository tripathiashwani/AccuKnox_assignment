# Generated by Django 5.0 on 2024-07-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0007_alter_user_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="media/avatars\\highschool_result_0XxNDY5.jpg",
                null=True,
                upload_to="avatars",
            ),
        ),
    ]
