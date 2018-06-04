from django.contrib import admin
from .models import Posts

# class AdminPost(admin.ModelAdmin):  For automatic blank field slug. slug = model.SlugField()
#     prepopulated_fields = {'slug': ('title')}


# admin.site.register(Posts, AdminPost)

admin.site.register(Posts)
