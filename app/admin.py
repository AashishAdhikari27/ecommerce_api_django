from django.contrib import admin
from django.core.exceptions import ValidationError


from django.contrib.auth import get_user_model

User = get_user_model()








class UserAdmin(admin.ModelAdmin):

    list_display = [
        'username', 'email', 'first_name', 'last_name', 'role', 
        'is_staff', 'is_active', 'date_joined', 'last_login'
    ]

    list_filter = ['role', 'is_staff', 'is_active', 'date_joined']

    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    ordering = ['-date_joined']
    
    readonly_fields = ['date_joined', 'last_login']


    # This below inbuilt save_model() function work properly
    def save_model(self, request, obj, form, change):

        if not obj.username and obj.email:
            obj.username = obj.email.split('@')[0].lower()

        obj.email = obj.email.lower()

        if self.model.objects.filter(email__iexact=obj.email).exclude(pk=obj.pk).exists():
            raise ValidationError("A user with that email already exists.")
        
        super().save_model(request, obj, form, change)









admin.site.register(User, UserAdmin)
