# Generated by Django 2.0.5 on 2018-05-10 15:54

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20180510_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='body',
            field=wagtail.core.fields.RichTextField(blank=True),
        ),
    ]
