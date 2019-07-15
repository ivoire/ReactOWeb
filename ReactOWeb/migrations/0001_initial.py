# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-27 13:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("topic", models.TextField(db_index=True)),
                ("uuid", models.TextField(db_index=True)),
                ("datetime", models.DateTimeField(db_index=True)),
                ("username", models.TextField(db_index=True)),
                ("data", models.TextField()),
            ],
            options={"managed": False, "db_table": "messages"},
        )
    ]
