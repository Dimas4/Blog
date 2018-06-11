from django.contrib import admin
from .models import Category, Posts

# class AdminPost(admin.ModelAdmin):  For automatic blank field slug. slug = model.SlugField()
#     prepopulated_fields = {'slug': ('title')}


# admin.site.register(Posts, AdminPost)

admin.site.register(Category)
admin.site.register(Posts)
