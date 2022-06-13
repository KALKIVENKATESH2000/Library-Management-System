from django.db import models
from django.conf import settings

# Create your models here.
class Bookmodel(models.Model):
    bookname= models.CharField(max_length=50)
    author=models.CharField(max_length=50)
    published=models.DateField()
    bookcount=models.IntegerField(null=True)

    def __str__(self):
        return self.bookname

class Request_book(models.Model):
    student_name = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,)
    book_name=models.ForeignKey(Bookmodel,on_delete=models.CASCADE)
    request_date=models.DateField()
    bookissue_status = [
    ('Pending', 'Pending'),
    ('Cancelled', "Cancelled"),
    ('Approved', 'Approved')]
    status = models.CharField(max_length=20,choices=bookissue_status,default='pending')

    
    def __str__(self):
        return str(self.book_name)