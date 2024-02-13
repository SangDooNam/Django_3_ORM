from django.db import models
from django.core.exceptions import ValidationError


def less_than_five(value):
    """Raire an error if the value is 5 or greater."""
    if value >= 5:
        raise ValidationError("The price must be lower than 5 euros.")


class Song(models.Model):
    """The Song model."""

    STYLES = (
        ("Indie", "Indie"),
        ("Pop", "Pop"),
        ("Rock", "Rock"),
        ("Funky", "Funky"),
        ("Reggaeton", "Reggaeton"),
        ("Classic", "Classic"),
        ("Orquestra", "Orquestra"),
        ("Folk", "Folk")
    )

    audio = models.FileField(upload_to="audio")
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=50, db_index=True, null=True, blank=True)
    author_website = models.URLField(null=True, blank=True)
    album = models.CharField(max_length=250, null=True, blank=True)
    duration = models.DurationField()
    song_style = models.CharField(max_length=20, choices=STYLES, null=True, blank=True)
    playbacks = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=4, default=0,
                                validators=[less_than_five])
    deal_of_the_day = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        """Metadata."""

        constraints = [
            models.UniqueConstraint(fields=["title", "author", "album",
                                            "duration"],
                                    name="unique_song")
        ]
