import binascii
import os
from random import randint, shuffle

from django.db import models
from django.db.models import Max


class Card(models.Model):
    number = models.fields.IntegerField(primary_key=True)

    def __str__(self):
        return f"Card {self.number} ({self.words.count()})"

    @property
    def words_list(self):
        return list(self.words.all().values_list('word', flat=True))

    @property
    def words_list_with_description(self):
        return list(self.words.all().values('word', 'description'))

    @property
    def words_list_shuffled(self):
        words = self.words_list
        shuffle(words)
        return words

    def json(self):
        return {'card': self.number, 'words': self.words_list_shuffled}

    @staticmethod
    def random():
        max_number = Card.objects.all().aggregate(max_id=Max("number"))['max_id']
        while True:
            pk = randint(1, max_number)
            card = Card.objects.get(number=pk)
            if card:
                return card


class Category(models.Model):
    name = models.fields.CharField(max_length=32)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Pack(models.Model):
    name = models.fields.CharField(max_length=32)

    def __str__(self):
        return self.name


class Word(models.Model):
    word = models.fields.CharField(max_length=50)
    description = models.fields.CharField(blank=True, max_length=512)
    category = models.ForeignKey(
        Category,
        related_name="words",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    card = models.ForeignKey(
        Card,
        related_name="words",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    pack = models.ForeignKey(
        Pack,
        related_name="words",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.word} ({self.category.name if self.category else ''}) @ {self.pack.name if self.pack else ''}"


def random_secret(length: int = 16) -> str:
    return binascii.b2a_hex(os.urandom(length // 2)).decode()


class Session(models.Model):
    last_activity = models.fields.DateTimeField(auto_now=True)
    started = models.fields.DateTimeField(auto_now_add=True)

    secret = models.fields.CharField(max_length=16, default=random_secret)
    used_cards = models.ManyToManyField(Card, blank=True)
