from django.contrib import admin

# Register your models here.
from news.models import Category, News, Images

class NewsImageInline(admin.TabularInline):#image tablosundan 5 tane alan düzenleme ve oluşturma
    model = Images
    extra = 5

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['status']

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','status']
    list_filter = ['status','category']
    inlines = [NewsImageInline]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'news','image']

admin.site.register(Category,CategoryAdmin)
admin.site.register(News,NewsAdmin)
admin.site.register(Images,ImagesAdmin)