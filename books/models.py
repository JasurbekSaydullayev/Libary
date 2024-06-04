from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.title


class StarsBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='stars_book')
    star = models.IntegerField(default=0)
    sum_rate = models.IntegerField(default=0)
    number_of_raters = models.IntegerField(default=0)

    def __str__(self):
        return self.book

    @property
    def average_rating(self):
        if self.number_of_raters > 0:
            return self.sum_rate / self.number_of_raters
        return 0


class StarsOfUsers(models.Model):
    from user.models import User
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='stars')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars')
    star = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username

