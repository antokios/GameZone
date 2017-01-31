from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Game(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    image_bar = models.ImageField(null=True)
    category = models.ForeignKey('Category', null=True)
    developer = models.ForeignKey('Developer', null=True)
    description = models.TextField()
    short_description = models.CharField(max_length=450, null=True)
    official_page = models.URLField(blank=True, null=True)
    official_trailer = models.URLField(blank=True, null=True)
    announced = models.CharField(max_length=20, blank=True, null=True)
    released_date = models.DateField(blank=True, null=True)
    console = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=50)
    desc = models.TextField(blank=True, null=True)   #maybe a sort description for category

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=50)
    official_page = models.URLField(blank=True, null=True)  #link for official site
    image = models.ImageField(null=True)


    def __str__(self):
        return self.name


class Game_Review(models.Model):
    title = models.CharField(max_length=50, null=True)
    game = models.ForeignKey('Game', null=True)
    author = models.ForeignKey('auth.User')
    review = models.TextField()
    gameplay_video = models.URLField(blank=True, null=True)
    gameplay_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)
    graphics_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)
    story_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def publishReview(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def total_score(self):
        return int(round((self.gameplay_score+self.graphics_score+self.story_score)/3))


class Video(models.Model):
    title = models.CharField(max_length=100, null=True)
    game = models.ForeignKey('Game', null=True)
    link = models.URLField()

    def __str__(self):
        return self.title
