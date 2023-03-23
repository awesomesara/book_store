from django.db import models
from account.models import User


class BooksModel(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey('AuthorModel', on_delete=models.CASCADE)
    publisher = models.ForeignKey(User, on_delete=models.CASCADE)
    public_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    @property
    def get_image(self):
        return self.images.first()

    def get_absolute_url(self):
        from django.shortcuts import reverse
        return reverse('detail', kwargs={'pk': self.pk})


class AuthorModel(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.name



class Image(models.Model):
    image = models.ImageField(upload_to='books')
    book = models.ForeignKey(BooksModel, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return self.image.url