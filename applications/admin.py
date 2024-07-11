from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Prefix, Status, CustomUser, Application, MinecraftUser, News, ServerEvent
from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.models import User

# Register your models here.



class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        try:
            existing_user = obj.user  # Использование указанного пользователя в объекте CustomUser
            custom_user = CustomUser.objects.create(
                user=existing_user,
                nickname=existing_user.username,  # Используйте имя пользователя в качестве nickname или любое другое значение
                # Другие поля модели CustomUser
            )
        except CustomUser.DoesNotExist:
            print("Ошибка: объект CustomUser не найден.")
            
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(News)

admin.site.register(MinecraftUser)
admin.site.register(Prefix)
admin.site.register(Status)
admin.site.register(Application)
admin.site.register(ServerEvent)