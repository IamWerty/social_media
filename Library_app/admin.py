from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Book)
admin.site.register(BookComment)
admin.site.register(Chapter)
admin.site.register(ChapterComment)
admin.site.register(Channel)
admin.site.register(Post)
admin.site.register(Repost)
admin.site.register(Tag)