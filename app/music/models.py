from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Q 

def curret_year():
    
    return datetime.today().year


def less_than_five(value):
    """Raire an error if the value is 5 or greater."""
    if value >= 5:
        raise ValidationError("The price must be lower than 5 euros.")


class Author(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True)
    first_appearance = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1000), MaxValueValidator(curret_year)])
    last_appearance = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1000), MaxValueValidator(curret_year)])
    def clean(self):
        if self.first_appearance and self.last_appearance and self.last_appearance < self.first_appearance:
            raise ValidationError({'first_appearance': 'first_appearance can not be bigger then last_appearance.'})
        super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Album(models.Model):
    title = models.CharField(max_length=255)
    year_of_release = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(curret_year)])
    produced_by = models.CharField(blank=True, max_length=255, )
    
    def clean(self):
        if Q(year_of_release__isnull=True):
            raise ValidationError({'year_of_release': "year_of_release can't be set null."})
        super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.produced_by
    
    
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
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True, blank=True, related_name='author_reverse')
    author_website = models.URLField(null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True, related_name='album_reverse')
    duration = models.DurationField()
    style = models.CharField(max_length=20, choices=STYLES, null=True, blank=True)
    playbacks = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=4, default=0,
                                validators=[less_than_five])
    deal_of_the_day = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        """Metadata."""

        constraints = [
            models.UniqueConstraint(fields=["title", "author", "album",
                                            "duration"],
                                    name="unique_song")
        ]
    def clean(self):
        if Q(duration__isnull=True):
            raise ValidationError({'duration': "Duration can't be set Null"})
        super().clean()
    
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Musician(models.Model):
    INSTRUMENTS = (
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
    )
    name = models.CharField(max_length=150)
    nationality = models.CharField(max_length=2)
    instrument = models.CharField(choices=INSTRUMENTS)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='members')

    def clean(self):
        if len(self.name) > 150:
            raise ValidationError({"name": "name can contain not more 150 letters."})
        super().clean()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        
        super().save(*args, **kwargs)
        


# Task 2

"""
1.
song_46 = Song.objects.get(id=46)
Musician.objects.filter(author_id=song_46.author_id)
"""

"""
2.
song_13 = Song.objects.get(id=13)
Album.objects.filter(id=song_13.album_id)
"""

"""
3.

sax_players = Musician.objects.filter(instrument='sax')

In [12]: id_lst = []

In [13]: for sax_player in sax_players:
    ...:     id_lst.append(sax_player.author_id)
    ...: 

In [14]: id_lst
Out[14]: 
[5,
 20,
 20,
 22,
 25,
 26,
 27,
 29,
 30,
 30,
 31,
 44,
 46,
 47,
 57,
 62,
 65,
 67,
 67,
 75,
 75,
 81,
 89,
 100]
 
Song.objects.filter(style='Pop', author_id__in= id_lst).all().values('pk','title','album__title')

Song.objects.filter(style='Pop', author_id__in= id_lst).all().values('pk','title','album__title').count()
"""


"""
4.


In [25]: clark_albums = Album.objects.filter(produced_by = 'Clark')

In [26]: clark_lst = []

In [27]: for album in clark_albums:
    ...:     clark_lst.append(album.id)
    ...: 

In [28]: sax_players = Musician.objects.filter(instrument='sax')

In [29]: sax_lst = []

In [30]: for sax_player in sax_players:
    ...:     sax_lst.append(sax_player.author_id)

In [31]: Song.objects.filter(author_id__in=sax_lst, album_id__in=clark_lst).all().values('pk','title','album__title')
In [32]: Song.objects.filter(author_id__in=sax_lst, album_id__in=clark_lst).all().values('pk','title','album__title').count()
"""

"""
5.

In [49]: today_year = datetime.today().year

In [50]: hundred_years_ago = today_year - 100

In [51]: from django.db.models import Q

In [52]: Album.objects.filter(Q(year_of_release__gte=hundred_years_ago) & Q(year_of_release__lte=today_year)).values('produced_by')

In [53]: Album.objects.filter(Q(year_of_release__gte=hundred_years_ago) & Q(year_of_release__lte=today_year)).values('produced_by').count()


"""