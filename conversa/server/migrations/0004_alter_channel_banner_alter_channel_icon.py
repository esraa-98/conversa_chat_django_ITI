# Generated by Django 4.2.7 on 2023-11-12 20:54

from django.db import migrations, models
import server.models
import server.validators


class Migration(migrations.Migration):
    dependencies = [
        ("server", "0003_channel_banner_channel_icon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="banner",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=server.models.server_banner_upload_path,
                validators=[server.validators.validate_image_file_extension],
            ),
        ),
        migrations.AlterField(
            model_name="channel",
            name="icon",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=server.models.server_icon_upload_path,
                validators=[
                    server.validators.validate_icon_image_size,
                    server.validators.validate_image_file_extension,
                ],
            ),
        ),
    ]
