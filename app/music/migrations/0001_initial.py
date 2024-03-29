# Generated by Django 4.2.7 on 2024-02-14 23:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import music.models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Album",
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
                ("title", models.CharField(max_length=255)),
                (
                    "year_of_release",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(1000),
                            django.core.validators.MaxValueValidator(
                                music.models.curret_year
                            ),
                        ]
                    ),
                ),
                ("produced_by", models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Author",
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
                ("name", models.CharField(max_length=255)),
                ("website", models.URLField(blank=True)),
                (
                    "first_appearance",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1000),
                            django.core.validators.MaxValueValidator(
                                music.models.curret_year
                            ),
                        ],
                    ),
                ),
                (
                    "last_appearance",
                    models.IntegerField(
                        blank=True,
                        null=True,
                        validators=[
                            django.core.validators.MinValueValidator(1000),
                            django.core.validators.MaxValueValidator(
                                music.models.curret_year
                            ),
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Song",
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
                ("audio", models.FileField(upload_to="audio")),
                ("title", models.CharField(max_length=250)),
                ("author_website", models.URLField(blank=True, null=True)),
                ("duration", models.DurationField()),
                (
                    "style",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("Indie", "Indie"),
                            ("Pop", "Pop"),
                            ("Rock", "Rock"),
                            ("Funky", "Funky"),
                            ("Reggaeton", "Reggaeton"),
                            ("Classic", "Classic"),
                            ("Orquestra", "Orquestra"),
                            ("Folk", "Folk"),
                        ],
                        max_length=20,
                        null=True,
                    ),
                ),
                ("playbacks", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        default=0,
                        max_digits=4,
                        validators=[music.models.less_than_five],
                    ),
                ),
                ("deal_of_the_day", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                (
                    "album",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="album_reverse",
                        to="music.album",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="author_reverse",
                        to="music.author",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Musician",
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
                ("name", models.CharField(max_length=150)),
                ("nationality", models.CharField(max_length=2)),
                (
                    "instrument",
                    models.CharField(
                        choices=[
                            ("piano", "Piano"),
                            ("eguitar", "Electric Guitar"),
                            ("cguitar", "Classical Guitar"),
                            ("aguitar", "Acoustic Guitar"),
                            ("ebass", "Electric Bass"),
                            ("bass", "Bass"),
                            ("drums", "Drums"),
                            ("voice", "Voice"),
                            ("violin", "Violin"),
                            ("harp", "Harp"),
                            ("handpan", "Handpan"),
                            ("tambourine", "Tambourine"),
                            ("sax", "Saxophone"),
                            ("trumpet", "Trumpet"),
                            ("trombone", "Trombone"),
                            ("flute", "Flute"),
                            ("clarinet", "Clarinet"),
                            ("ukulele", "Ukulele"),
                        ]
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="members",
                        to="music.author",
                    ),
                ),
            ],
        ),
        migrations.AddConstraint(
            model_name="song",
            constraint=models.UniqueConstraint(
                fields=("title", "author", "album", "duration"), name="unique_song"
            ),
        ),
    ]
