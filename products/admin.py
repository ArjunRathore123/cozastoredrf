from django.contrib import admin
from .models import Product,Category,Size,sizes,Cart,Order
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','product_image','category',sizes,'price','quantity','description',"created_at")

    fieldsets=((None,{"fields":('product_name','product_image','category','size','price','quantity','description',"created_at")}),
              
               )
    add_fieldsets=(
        (None,{'classes':("wide",),
               'fields':('product_name','product_image','category','size','price','quantity','description',"created_at")},
        )
    )
    search_fields=('product_name',)
    ordering=('product_name',)

  

    
admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Size)
admin.site.register(Cart)
admin.site.register(Order)
