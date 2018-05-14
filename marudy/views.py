from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Maruda, MarudaVoting
from django.utils import timezone

def home(request):
    marudy = Maruda.objects

    marudalist = list()
    if request.user.is_authenticated:
        for element in User.objects.get(id = request.user.id).voted_by.all():
            marudalist.append(element.maruda)

    return render(request, 'marudy/home.html', {'marudy':marudy, 'marudalist':marudalist})

def topfive(request):
    marudy = Maruda.objects.order_by('-votes_total')

    marudalist = list()
    if request.user.is_authenticated:
        for element in User.objects.get(id = request.user.id).voted_by.all():
            marudalist.append(element.maruda)

    return render(request, 'marudy/topfive.html', {'marudy':marudy[:5], 'marudalist':marudalist})

@login_required(login_url = "/accounts/login")
def create(request):
    if request.method == "POST":
        if request.POST['title'] and request.POST['text'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            maruda = Maruda()
            maruda.title = request.POST['title']
            maruda.text = request.POST['text']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                maruda.url = request.POST['url']
            else:
                maruda.url = 'http://' + request.POST['url']
            maruda.icon = request.FILES['icon']
            maruda.image = request.FILES['image']

            maruda.date = timezone.datetime.now()
            #maruda.votes_total = 1
            maruda.hunter = request.user
            maruda.save()
            return redirect('/marudy/' + str(maruda.id))
        else:
            return render(request, 'marudy/create.html', {'error':'All fields are required'})

    else:
        return render(request, 'marudy/create.html')


def detail(request, maruda_id):
    maruda = get_object_or_404(Maruda, pk = maruda_id)

    userlist = list()
    if request.user.is_authenticated:
        for element in Maruda.objects.get(id = maruda.id).voted.all():
            userlist.append(element.voting)

    return render(request, 'marudy/detail.html', {'maruda':maruda, 'userlist':userlist})

@login_required(login_url = "/accounts/login")
def upvote(request, maruda_id):
    if request.method == "POST":
        thismaruda = get_object_or_404(Maruda, pk = maruda_id)
        #tutaj wstaw logike do glosowania tylko raz
        #sciagnij z maruda voting te elementy gdzie jest ta sama maruda
        #nastepnie porownaj czy w tych elementach jest aktualnie zalogowany uzytkownik
        userlist = list()
        for element in Maruda.objects.get(id = thismaruda.id).voted.all():
            userlist.append(element.voting)

        if request.user in userlist:
            thismaruda.votes_total -= 1
            thismaruda.save()
        #jeeli tak, to odejmij 1 od maruda.votes_total i usun element wspolny w MarudaVoting
            get_object_or_404(MarudaVoting, voting = request.user, maruda = thismaruda).delete()

        else:
            thismaruda.votes_total += 1
            thismaruda.save()
        #jezeli nie, to dodaj 1 do maruda.votes_total i dodaj element wspolny w MarudaVoting
            addLinkMaruda = MarudaVoting()
            addLinkMaruda.maruda = thismaruda
            addLinkMaruda.voting = request.user
            addLinkMaruda.save()


        return redirect('/marudy/' + str(maruda_id))
