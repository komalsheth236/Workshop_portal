from django.contrib import messages
from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from website.models import Workshop, Slot, Booking
from website.forms import WorkshopForm, UserLoginForm, UserRegisterForm, SlotsForm, BookslotForm
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.context import RequestContext
from django.contrib.auth.decorators import login_required


def home(request):
   return render(request, "base.html")


def user_login(request):
	if request.method == "POST":
		context = {}
		context.update(csrf(request))
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			if 'next' in request.GET:
				next = request.GET['next']
				return HttpResponseRedirect(next)
			else:
				pass
			context['user'] = user
			ws = Workshop.objects.all().order_by("date_modified").reverse()
			for w in ws:
				tags = str(w.tag)
			try:
				tag_list = w.tag.split(",")
				w.tag = tag_list
			except:
				pass
			context['ws']= ws
			return render_to_response('table.html', context)
		else:
			context['invalid'] = True
			context['form'] = UserLoginForm
			context['user'] = user
			return render_to_response('login.html', context)
	else:
		form = UserLoginForm()
		context = RequestContext(request, {'request': request,
                                           'user': request.user,
                                           'form': form})
		context.update(csrf(request))
		return render_to_response('login.html',
                             context_instance=context)


def userregister(request):
    context = {}
    context.update(csrf(request))
    registered_emails = []
    users = User.objects.all()
    for user in users:
        registered_emails.append(user.email)
    if request.user.is_anonymous():
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['email'] in registered_emails:
                    context['form'] = form
                    context['email_registered'] = True
                    return render_to_response('user-register.html', context)
                else:
                    form.save()
                    context['registration_complete'] = True
                    form = UserLoginForm()
                    context['form'] = form
                    context['user'] = request.user
                    return render_to_response('table.html', context)
            else:
                context.update(csrf(request))
                context['form'] = form
                return render_to_response('user-register.html', context)
        else:
            form = UserRegisterForm()
        context.update(csrf(request))
        context['form'] = form
        return render_to_response('user-register.html', context)
    else:
        context['user'] = request.user
        return render_to_response('table.html', context)


def table(request):
	context = {}
	context.update(csrf(request))
	user = request.user
	ws = Workshop.objects.all().order_by("date_modified").reverse()
	for w in ws:
		tags = str(w.tag)
		try:
			tag_list = w.tag.split(",")
			w.tag = tag_list
		except:
			pass
	context['ws']= ws
	context['user'] = user
	return render(request, "table.html", context)


def details(request, workshop_id= None):
	context ={}
	context.update(csrf(request))
	user = request.user
	instance = get_object_or_404(Workshop, id = workshop_id)
	context['instance'] = instance
	context['user'] = user
	return render(request, "details.html", context)


@login_required
def add_workshop(request):
	user = request.user
	context = {}
	context.update(csrf(request))
	form = WorkshopForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit = False)
		instance.save()
		messages.success(request, "Added Successfully")
		ws = Workshop.objects.all()
		context['ws']= ws
		context['user'] = user
		return HttpResponseRedirect(instance.get_absolute_url())
	# if request.method == 'POST':
	context = {}
	context['form'] = form
	return render(request, "add_workshop.html", context)


@login_required
def slots(request, workshop_id = None):
	context ={}
	context.update(csrf(request))
	instance = get_object_or_404(Workshop, id = workshop_id)
	workshop = Workshop.objects.get(id = instance.id)
	form = SlotsForm(request.POST)
	if request.method == 'POST':
		if 'add_slot' in request.POST:
			if form.is_valid():
				data = form.cleaned_data
				data = form.save(commit=False)
				data.user = request.user
				data.workshop = workshop
				data.status = 'A'
				data.save()
			else:
				context.update(csrf(request))
				context['form'] = form
				return render_to_response('slots.html', contex)
		elif 'delete' in request.POST:
			# form = SlotsForm(request.POST)
			delete_slots = request.POST.getlist('delete_slot')
			for slot_id in delete_slots:
				slot = Slot.objects.get(id = int(slot_id))
			 	slot.delete()
			context.update(csrf(request)) 
	else:
		form = SlotsForm()
	slots = Slot.objects.all()
	user = request.user
	context['instance'] = instance
	context['form']= form
	context['user'] = user
	context['slots'] = slots
	return render(request, "slots.html", context)


@login_required
def book_slot(request, workshop_id= None):
	context ={}
	context.update(csrf(request))
	user = request.user
	instance = get_object_or_404(Workshop, id = workshop_id)
	slots = Slot.objects.filter(workshop = workshop_id, status = "A")
	form = BookslotForm(request.POST)
	if request.method == 'POST':
		if 'book' in request.POST:
			if form.is_valid():
				print "form is valid"
				slot_id = request.POST.get('book_slot')
				data = form.cleaned_data
				print "address", data
				print "slot id",slot_id
				data = form.save(commit=False)
				user_slot = Slot.objects.get(id = slot_id)
				data.slot = user_slot
				data.user = user
				context['user_slot'] = user_slot
				context['user'] = user
				context['booked'] = True
				user_slot.status = 'P'
				user_slot.save()
				data.save()
				return HttpResponseRedirect(instance.get_absolute_url())
			else:
				print "form valid else"
				context.update(csrf(request))
				context['form'] = form
				context['slots'] = slots
				context['instance'] = instance
				return render(request, 'book_slot.html', context)
		else:
			print "book in request else "
			form = BookslotForm()
	else:
		print "request method else"
		form = BookslotForm()
	context['slots'] = slots
	context['form'] = form
	context['instance'] = instance
	return render(request, 'book_slot.html', context)


@login_required
def slot_details(request, slot_id = None):
	context ={}
	context.update(csrf(request))
	print "slot_id", slot_id
	instance = get_object_or_404(Booking, slot_id = slot_id)
	workshop_id = instance.slot.workshop.id
	instancew = get_object_or_404(Workshop, id = workshop_id)
	if request.method == 'POST':
		if 'approve' in request.POST:
			approve_slot = Slot.objects.get(id = slot_id)
			approve_slot.status = 'NA'
			approve_slot.save()
		elif 'disapprove' in request.POST:
			approve_slot = Slot.objects.get(id = slot_id)
			approve_slot.status = 'A'
			approve_slot.save()
		slots = Slot.objects.all()
		form = SlotsForm()
		context['slots'] = slots
		context['form'] = form
		return HttpResponseRedirect(instance.get_absolute_url())
	context['instance'] = instance
	return render (request, 'slot_details.html', context)


@login_required
def edit_workshop(request, workshop_id= None):
	context ={}
	context.update(csrf(request))
	instance = get_object_or_404(Workshop, id = workshop_id)
	form = WorkshopForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		print 
		instance = form.save(commit = False)
		instance.save()
		return HttpResponseRedirect(instance.get_absolute_url())
	context['instance'] = instance
	context['form'] = form
	return render(request, "edit_workshop.html", context)


@login_required
def delete(request, workshop_id = None):
	instance = get_object_or_404(Workshop, id = workshop_id)
	instance.delete()
	return redirect("website:table")

