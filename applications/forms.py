from django import forms
from .models import Application
from .models import MinecraftUser, News
from .models import ServerEvent



class ApplicationForm(forms.ModelForm):
    nickname = forms.CharField(label='Ваш игровой Ник-Нейм', required=True, widget=forms.TextInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Ник-Нейм"}))
    age = forms.CharField(label='Возраст', required=True, widget=forms.NumberInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Возраст"}))
    source = forms.CharField(label='Из какого источника узнали о проекте', required=True, widget=forms.TextInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Источник"}))
    previous_projects = forms.CharField(label='На каких проектах вы участвовали до этого? Из-за чего вы ушли оттуда?', required=True, widget=forms.TextInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Предыдущие проекты"}))
    activities = forms.CharField(label='Что вы обычно делаете на таких серверах? Чем вы планируете заниматься здесь?', required=True, widget=forms.TextInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Активность"}))
    read_rules = forms.CharField(label='Тщательно ли вы читали правила? Готовы ли вы соблюдать их? ', required=True, widget=forms.TextInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Правила"}))
    communication_style = forms.CharField(label=' Вы коммуникабельный человек? Какой стиль игры вы предпочитаете? (Одиночный, командный)', required=True, widget=forms.TextInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Стиль игры"}))
    participate_in_storyline =  forms.CharField(label='Хотели бы вы участвовать в сюжетной линии проекта?', required=False, widget=forms.TextInput(attrs={ 'style': 'border: none; border-bottom: 2px solid #D1D1D4; background: none; padding: 10px; padding-left: 24px; font-weight: 700; width: 75%; transition: .2s; outline: none; border-bottom-color: #6A679E; ', 'placeholder': "Сюжет"}))




    class Meta: 
        model = Application
        fields = ['nickname', 'age', 'source', 'previous_projects', 'activities', 'read_rules', 'communication_style', 'participate_in_storyline']

        



class MinecraftUserForm(forms.ModelForm):
    class Meta:
        model = MinecraftUser
        fields = ['user', 'nickname', 'prefix', 'status']

    def __init__(self, *args, **kwargs):
        super(MinecraftUserForm, self).__init__(*args, **kwargs)
        self.fields['status'].required = False  # Сделать поле необязательным


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'description', 'content', 'image', 'author']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }


class ServerEventForm(forms.ModelForm):
    class Meta:
        model = ServerEvent
        fields = ['title', 'description', 'status', 'date']