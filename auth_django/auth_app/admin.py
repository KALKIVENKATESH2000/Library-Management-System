from django.contrib import admin
from .models import Bookmodel, Request_book

# Register your models here.
class Librarydmin(admin.ModelAdmin):
    list_display= ["bookname","author","published"]
    def __str__(self):
        return self.bookname

admin.site.register(Bookmodel,Librarydmin)

class Request_book_admin(admin.ModelAdmin):
    list_display=["student_name","book_name",'request_date','status']
 
admin.site.register(Request_book,Request_book_admin)

