from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import Bookmodel, Request_book
from .forms import UserRegisterForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from datetime import datetime
from django.http import HttpResponse


def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			user=form.save()
			if request.POST['usertype']=='librarian':
				user.is_staff=True
				user.save()
			else:
				user.is_staff=False
				user.save()
			login(request, user)
			return redirect('signup')
		messages.error(request, "Unsuccessful registration. invalid information.")
	else:
		form = UserRegisterForm()
	return render(request, 'register.html', {'form': form})



def signup(request):
	if request.method == "POST":
		form = AuthenticationForm(request,request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request,"valid username or password.")
				if user.is_staff==True:
					return redirect('librarian')
				#elif user.is_staff==False:
					#return redirect('student')
				else:
					return redirect('student')
				
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request,"login.html", {"login_form":form})

def logout_view(request):
	logout(request)
	messages.info(request, f'You have successfully logout')
	return redirect('register')

def librarian(request):
	book=Bookmodel.objects.all()
	return render(request,'librarian.html', {'book':book})

#def student(request):
 #   return render(request, 'student.html')

def add(request):
	if request.method=="GET":
		return render(request,'addbook.html')
	else:
		Bookmodel(
			bookname=request.POST.get('bname'),
			author=request.POST.get('aname'),
   			published= request.POST.get('date')
		).save()
		return redirect('librarian')
def update(request,id):
	if request.method=="GET":
		updatebook=Bookmodel.objects.get(id=id)
		return render(request,'update.html',{'updatebook':updatebook})
	else:
		updatebook=Bookmodel.objects.get(id=id)
		updatebook.bookname=request.POST['bname']
		updatebook.author=request.POST['aname']
		updatebook.published= request.POST['date']
		updatebook.save()
		return redirect('librarian')

def deletebook(request,id):
	delbook=Bookmodel.objects.get(id=id)
	delbook.delete()
	return redirect('librarian')

def request_book(request):
	if request.user.is_staff==False:
		bookslist = Bookmodel.objects.filter(bookcount__gt = 0)
		
		if request.method == "POST" :
			update_book_name = Bookmodel.objects.get(id = request.POST['req_book'])
			Request_book.objects.create(book_name = update_book_name, student_name = request.user, request_date = datetime.now(), status = "Pending")
			
			
		return render(request,'student.html',{'bookslist':bookslist})
			 
	else:
		return HttpResponse('Has no access to request book')
def booklist(request):
	book=Bookmodel.objects.all()
	return render(request,'booklist.html',{'book':book})


def issuebook(request):
	pending_book=Request_book.objects.filter(status="Pending")
	return render(request,'pending.html',{'pending_book':pending_book})

def approvebook(request,id):
	approve_book=Request_book.objects.get(id=id)
	approve_book.status="Approved" 
	approve_book.save()
	book=Bookmodel.objects.get(bookname=approve_book.book_name)
	book.bookcount=book.bookcount-1
	book.save()
	return render(request,'approve.html',{'approve_book':approve_book})
def decline(request,id):
	decline_req=Request_book.objects.get(id=id)
	decline_req.status="Cancelled"
	decline_req.save()
	return redirect('/issuebook')
