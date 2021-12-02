# Generated by Django 3.2 on 2021-10-08 15:13

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("core_main_app", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExportedCompressedFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("file_name", models.CharField(max_length=200)),
                (
                    "file",
                    models.FileField(
                        blank=True, null=True, upload_to="exporter_compressed_files"
                    ),
                ),
                ("is_ready", models.BooleanField(default=False)),
                ("mime_type", models.CharField(max_length=200)),
                ("user_id", models.CharField(max_length=200)),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Exporter",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=200,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                code="invalid_title",
                                message="Title must not be empty or only whitespaces",
                                regex=".*\\S.*",
                            )
                        ],
                    ),
                ),
                ("url", models.CharField(max_length=200)),
                ("enable_by_default", models.BooleanField()),
                ("_cls", models.CharField(default="Exporter", max_length=200)),
                (
                    "templates",
                    models.ManyToManyField(blank=True, to="core_main_app.Template"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ExporterXsl",
            fields=[
                (
                    "exporter_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="core_exporters_app.exporter",
                    ),
                ),
                (
                    "xsl_transformation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core_main_app.xsltransformation",
                    ),
                ),
            ],
            bases=("core_exporters_app.exporter",),
        ),
    ]
