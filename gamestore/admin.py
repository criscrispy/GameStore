from django.contrib import admin

from .models import *


class GameAdmin(admin.ModelAdmin):
    model = Game
    list_display = ('publisher', 'title', 'description', 'price', 'url',  'get_category_title')

    def get_category_title(self, obj):
        return obj.category.title
    get_category_title.short_description = 'Category'
    get_category_title.admin_order_field = 'category__title'


# Register your models here.
admin.site.register(Game, GameAdmin)
admin.site.register(Profile)
admin.site.register(Score)
admin.site.register(GameSale)
admin.site.register(Category)
