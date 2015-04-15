from django.shortcuts import render
from django.http import HttpResponse
from task.models import Employee
from task.models import Task
from task.models import Report
from task.models import Message
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response


def create_task(request):
	context_dict = {}
	employee = Employee.objects.get(pk=1)
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	if request.method == 'POST':
		title = request.POST['title']
		desc = request.POST['desc']
		date = request.POST['date']
		today = datetime.now().date()
		task = Task(owner=employee, date_published=today, date_due=date, title=title, description=desc, state=False)
		task.save()
	return render(request, 'task/create_task.html', context_dict)

@login_required
def list_of_tasks(request):
	context_dict = {}
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	tasks = Task.objects.filter(state=False).filter(owner=employee)
	context_dict['tasks'] = tasks
	return render(request, 'task/list_of_tasks.html', context_dict)

def create_report(request):
	context_dict = {}
	employee = Employee.objects.get(pk=1)
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	tasks = Task.objects.filter(state=False)
	context_dict['tasks'] = tasks
	post_reply = []
	context_dict['post_reply'] = post_reply
	if request.method == 'POST':
		task_id = request.POST['task_id']
		description = request.POST['description']
		task = Task.objects.get(pk=task_id)
		today = datetime.now().date()
		report = Report(owner = employee, date_published = today, description = description, task=task, title="")
		report.save()
		post_reply.append(5)
		context_dict['post_reply'] = post_reply
	return render(request, 'task/create_report.html', context_dict)

def send_message(request):
	context_dict = {}
	employee = Employee.objects.get(pk=1)
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	tasks = Task.objects.filter(state=False)
	context_dict['tasks'] = tasks
	post_reply = []
	context_dict['post_reply'] = post_reply
	if request.method == 'POST':
		task_id = request.POST['task_id']
		description = request.POST['description']
		task = Task.objects.get(pk=task_id)
		today = datetime.now().date()
		message = Message(owner = employee, date_published = today, text = description, task=task)
		message.save()
		post_reply.append(5)
		context_dict['post_reply'] = post_reply
	return render(request, 'task/send_message.html', context_dict)

def show_detail(request):
	context_dict = {}
	employee = Employee.objects.get(pk=1)
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	if request.method == 'GET':
		task_id = request.GET['task_id']
		task = Task.objects.get(pk=task_id)
		context_dict['task'] = task
		messages = Message.objects.filter(task=task)
		context_dict['messages'] = messages
	if request.method =='POST':
		task_id = request.POST['task_id']
		task = Task.objects.get(pk=task_id)
		context_dict['task'] = task
		description = request.POST['description']
		today = datetime.now().date()
		message = Message(owner = employee, date_published = today, text = description, task=task)
		message.save()
		messages = Message.objects.filter(task=task)
		context_dict['messages'] = messages
	return render(request, 'task/show_detail.html', context_dict)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                

                login(request, user)
                employee = Employee.objects.get(user=user)
                if employee.is_admin :
                	return HttpResponseRedirect('/task/admin/')
                return HttpResponseRedirect('/task/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("account disabled")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('task/login.html', {}, context)	

@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")

@login_required
def admin(request):
	context_dict = {}
	emps = []
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	employees = Employee.objects.all()
	for emp in employees:
		messages = Message.objects.filter(owner = emp).filter(is_seen=False)
		emps.append((emp, messages))
	context_dict['emps'] = emps
	return render(request, 'task/admin.html', context_dict)

@login_required
def admin_detail(request, emp_id=1):
	context_dict = {}
	emps = []
	emp = Employee.objects.get(pk = emp_id)
	context_dict['emp'] = emp
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	if request.method == 'GET':
		messages = Message.objects.filter(owner = emp)
		reports = Report.objects.filter(owner = emp)
		tasks = Task.objects.filter(owner = emp)
		context_dict['messages'] = messages
		context_dict['reports'] = reports
		context_dict['tasks'] = tasks
	return render(request, 'task/admin_detail.html', context_dict)

def admin_show_detail(request, emp_id=1):
	context_dict = {}
	employee = Employee.objects.get(pk=1)
	emp = Employee.objects.get(pk = emp_id)
	context_dict['emp'] = emp
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	if request.method == 'GET':
		task_id = request.GET['task_id']
		task = Task.objects.get(pk=task_id)
		context_dict['task'] = task
		messages = Message.objects.filter(task=task)
		context_dict['messages'] = messages
		for m in messages:
			m.is_seen = True
	if request.method =='POST':
		task_id = request.POST['task_id']
		task = Task.objects.get(pk=task_id)
		context_dict['task'] = task
		description = request.POST['description']
		today = datetime.now().date()
		message = Message(owner = employee, date_published = today, text = description, task=task)
		message.save()
		messages = Message.objects.filter(task=task)
		context_dict['messages'] = messages
	return render(request, 'task/admin_show_detail.html', context_dict)

def admin_create_task(request, emp_id=1):
	context_dict = {}
	employee = Employee.objects.get(pk=1)
	emp = Employee.objects.get(pk = emp_id)
	context_dict['emp'] = emp
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	if request.method == 'POST':
		title = request.POST['title']
		desc = request.POST['desc']
		date = request.POST['date']
		today = datetime.now().date()
		task = Task(owner=emp, date_published=today, date_due=date, title=title, description=desc, state=False)
		task.save()
	return render(request, 'task/admin_create_task.html', context_dict)

def admin_create_report(request, emp_id=1):
	context_dict = {}
	employee = Employee.objects.get(pk=1)
	emp = Employee.objects.get(pk = emp_id)
	context_dict['emp'] = emp
	if request.user.is_authenticated():
		username = request.user.username
		employee = Employee.objects.get(user=request.user)
		context_dict['employee'] = employee
	tasks = Task.objects.filter(state=False)
	context_dict['tasks'] = tasks
	post_reply = []
	context_dict['post_reply'] = post_reply
	if request.method == 'POST':
		task_id = request.POST['task_id']
		description = request.POST['description']
		task = Task.objects.get(pk=task_id)
		task.state = False
		post_reply.append(5)
		context_dict['post_reply'] = post_reply
	return render(request, 'task/admin_create_report.html', context_dict)



# Create your views here.
