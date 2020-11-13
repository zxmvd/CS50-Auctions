from django.contrib import admin
from .models import User, Listing, Bid, Comment, Category

class CategoryAdmin(admin.ModelAdmin):
    filter = ("parent_category", "listing")
    filter_horizontal = ("listing",)


admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)

# Register your models here.
