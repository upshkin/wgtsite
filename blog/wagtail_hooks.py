from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)

from blog.models import BlogPost


class MyBlogPageModelAdmin(ModelAdmin):
    model = BlogPost
    menu_label = 'Our blog'  # ditch this to use verbose_name_plural from model
    menu_icon = 'list-ul'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('thumb_image', 'title', 'intro', 'date', 'live')
    list_filter = ('live', 'date')
    search_fields = ('title', 'intro', 'body')
    list_per_page = 10
    list_display_add_buttons = 'title'


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(MyBlogPageModelAdmin)
