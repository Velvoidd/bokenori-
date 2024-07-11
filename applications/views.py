from django.shortcuts import render, redirect, get_object_or_404    
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage
from .forms import ApplicationForm
from .models import Application
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import MinecraftUser, Prefix, Status
from .models import DiscordInvitation
import uuid
from .models import Prefix, Status
from .forms import MinecraftUserForm
from .models import News
from .forms import NewsForm
from .models import ServerEvent
from .forms import ServerEventForm
from django.http import HttpResponseBadRequest
from .models import ChatMessage




@login_required
def base_view(request):
    if request.user.is_authenticated:
        return render(request, 'base.html')
    return redirect('index')

def index(request):
    if not request.user.is_authenticated:
        return redirect('welcome')  # Перенаправляем неавторизованных пользователей на страницу приветствия
    else:
        return render(request, 'index.html')


def registration_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')  # Замените 'index.html' на URL вашей главной страницы
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Авторизация
def login_site(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error_message': 'Неверное имя пользователя или пароль.'})
    return render(request, 'login.html')

@login_required
def logout_site(request):
    logout(request)
    return redirect('welcome')


def apply(request):
    existing_application = Application.objects.filter(user=request.user).first()
    
    # Проверяем, существует ли заявка для текущего пользователя
    if existing_application:
        status = existing_application.get_status_display()
        
        # Если заявка уже существует, и ее статус "Одобрено", создаем CustomUser
        if existing_application.status == 'approved':
            # Получаем или создаем CustomUser
            custom_user, created = get_user_model().objects.get_or_create(username=request.user.username)
            custom_user.nickname = existing_application.nickname
            custom_user.discord_link = existing_application.discord_link  # Добавляем сохранение ссылки на Discord
            custom_user.save()
            return render(request, 'custom_user_created.html', {'custom_user': custom_user})
        else:
            return render(request, 'application_exists.html', {'status': status})
    else:
        if request.method == 'POST':
            form = ApplicationForm(request.POST)
            if form.is_valid():
                application = form.save(commit=False)
                application.user = request.user
                application.save()
                return render(request, 'application_success.html')
        else:
            form = ApplicationForm()
        return render(request, 'apply.html', {'form': form})
    
def submit_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            # После успешной отправки заявки редиректим пользователя на нужную страницу, например, на главную
            return redirect('')
    else:
        form = ApplicationForm()
    return render(request, '', {'form': form})


@login_required
def application_success(request):
    # Проверяем, существует ли запись DiscordInvitation для текущего пользователя
    return render(request, 'application_success.html')



def applications_list(request):
    all_applications = Application.objects.all()
    paginator = Paginator(all_applications, 10)  # Пагинация по 10 записей на страницу

    page_number = request.GET.get('page', 1)  # Установка значения по умолчанию на 1, если параметр 'page' отсутствует
    try:
        applications = paginator.page(page_number)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)

    return render(request, 'applications_list.html', {'applications': applications})



def application_detail(request, pk):
    application = Application.objects.get(pk=pk)
    return render(request, 'application_detail.html', {'application': application})




def update_application_status(request, pk):
    # Получаем объект заявки или выводим ошибку 404, если объект не найден
    application = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        # Обрабатываем данные формы, отправленные методом POST
        new_status = request.POST.get('status')
        application.status = new_status
        application.save()
        # Перенаправляем пользователя обратно на страницу с деталями заявки
        return redirect('application_detail', pk=pk)
    else:
        # Если запрос не методом POST, просто показываем шаблон с формой для изменения статуса
        return render(request, 'update_application_status.html', {'application': application})




def application_exists(request):
    try:
        # Получаем текущего пользователя
        user = request.user
        # Пытаемся найти заявку пользователя
        application = Application.objects.get(user=user)
        # Получаем отображаемое значение статуса заявки
        status = application.get_status_display()
        return render(request, 'application_exists.html', {'status': status})
    except Application.DoesNotExist:
        # Если заявка не найдена, возвращаем пустой контекст
        return render(request, 'application_exists.html', {})
    



def profile_view(request, user_id):
    # Получаем пользователя по его ID
    user = User.objects.get(pk=user_id)
    if hasattr(user, 'customuser'):
        custom_user = user.customuser
    else:
        custom_user = None
    return render(request, 'profile.html', {'user': user, 'custom_user': custom_user})  

def custom_user_created(request):
    if request.method == 'POST':
        
        return redirect('application_success')
    else:
        
        try:
            discord_invitation = DiscordInvitation.objects.get(user=request.user)
        except DiscordInvitation.DoesNotExist:
            invite_link = DiscordInvitation.generate_invite_link()
            discord_invitation = DiscordInvitation.objects.create(user=request.user, invite_link=invite_link)

        return render(request, 'custom_user_created.html', {'invite_link': discord_invitation.invite_link})


def player_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        players = MinecraftUser.objects.filter(nickname__icontains=search_query)
    else:
        players = MinecraftUser.objects.all()
    return render(request, 'player_list.html', {'players': players})

def server_info(request):

    server_ip = "bokenori.online"


    context = {
        'server_ip': server_ip,
    }
    return render(request, 'info.html', context)


def rules_page(request):
    return render(request, 'rules.html')


def delete_application(request, pk):
    application = get_object_or_404(Application, pk=pk)
    if request.method == 'POST':
        application.delete()
        return redirect('applications_list')
    return render(request, 'application_delete.html', {'application': application})


def add_minecraft_user(request):
    users = User.objects.all()  
    prefixes = Prefix.objects.all() 
    statuses = Status.objects.all() 

    if request.method == 'POST':
        form = MinecraftUserForm(request.POST)
        if form.is_valid():
            selected_user_id = form.cleaned_data['user'].id
            selected_user = User.objects.get(id=selected_user_id)
            if not MinecraftUser.objects.filter(user=selected_user).exists():
                minecraft_user = form.save(commit=False)
                minecraft_user.user = selected_user
                minecraft_user.save()
                return redirect('user_added')
            else:
                form.add_error(None, "This user already exists.")
    else:
        form = MinecraftUserForm()

    return render(request, 'add_minecraft_user.html', {'form': form, 'users': users, 'prefixes': prefixes, 'statuses': statuses})

def user_added(request):
    users = MinecraftUser.objects.all()
    return render(request, 'added.html', {'users': users})


def player_list_adm(request):
    players = MinecraftUser.objects.all()
    return render(request, 'player_list_adm.html', {'players': players})


def edit_player(request, player_id):
    users = User.objects.all() 
    prefixes = Prefix.objects.all() 
    statuses = Status.objects.all() 
    
    player = get_object_or_404(MinecraftUser, id=player_id)
    if request.method == 'POST':
        form = MinecraftUserForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player_list_adm')
    else:
        form = MinecraftUserForm(instance=player)
    return render(request, 'edit_player.html', {'form': form, 'player': player, 'users': users, 'prefixes': prefixes, 'statuses': statuses})


def delete_player(request, player_id):
    player = get_object_or_404(MinecraftUser, id=player_id)
    if request.method == 'POST':
        player.delete()
        return redirect('player_list_adm')
    return render(request, 'confirm_delete.html', {'player': player})


def confirm_delete(request, player_id):
    player = MinecraftUser.objects.get(pk=player_id)
    return render(request, 'confirm_delete.html', {'player': player})



def news_list(request):
    news = News.objects.all()
    return render(request, 'news_list.html', {'news': news})

def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    return render(request, 'news_detail.html', {'news': news})

def update_application_status(request, pk):
    application = Application.objects.get(pk=pk)
    if request.method == 'POST':
        application.status = request.POST.get('status')
        application.discord_link = request.POST.get('discord_link')
        application.save()
        return redirect('application_detail', pk=pk)
    return render(request, 'application_detail.html', {'application': application})


def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()
            return redirect('news_detail', pk=news.pk)  # Меняем 'news_list' на 'news_detail'
    else:
        form = NewsForm()
    return render(request, 'create_news.html', {'form': form})



def welcome(request):
    return render(request, 'welcome.html')

def event_list(request):
    events = ServerEvent.objects.all()
    return render(request, 'event_list.html', {'events': events})

@login_required

def add_event(request):
    if request.method == 'POST':
        form = ServerEventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = ServerEventForm()
    return render(request, 'add_event.html', {'form': form})

@login_required

def edit_event(request, pk):
    event = get_object_or_404(ServerEvent, pk=pk)
    if request.method == 'POST':
        form = ServerEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=pk)
    else:
        form = ServerEventForm(instance=event)
    return render(request, 'edit_event.html', {'form': form, 'event': event})


def delete_event(request, pk):
    event = get_object_or_404(ServerEvent, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'event_delete.html', {'event': event})



def map_view(request):
    return render(request, 'map.html')


@login_required
def chat(request):
    messages = ChatMessage.objects.all().order_by('-timestamp')[:10]
    return render(request, 'chat.html', {'messages': messages})

@login_required
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            ChatMessage.objects.create(user=request.user, message=message)
    return redirect('chat')

@login_required
def get_messages(request):
    if request.method == 'GET' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        messages = ChatMessage.objects.all().order_by('-timestamp')[:10]
        data = [{'user': msg.user.username, 'message': msg.message, 'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')} for msg in messages]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error': 'Invalid request'})