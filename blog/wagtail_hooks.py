from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register
)
from wagtail.contrib.modeladmin.helpers import ButtonHelper, PageButtonHelper


from blog.models import BlogPost


class MyButtonHelper(PageButtonHelper):
    cn = ['button', 'button-small', 'button-secondary']

    def get_buttons_for_obj(self, obj, exclude=None, classnames_add=None,
                            classnames_exclude=None):
        btns = super(MyButtonHelper, self).get_buttons_for_obj(
                                                obj, classnames_add=self.cn)

        btns.insert(0, {
            'url': obj.url,
            'label': 'Открыть',
            'classname': ' '.join(self.cn),
            'title': 'Открыть материал "%s"' % obj.title,
            'target': 'blank',
        })

        return btns


class MyBlogPageModelAdmin(ModelAdmin):
    model = BlogPost
    menu_label = 'Blog'
    menu_icon = 'list-ul'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('thumb_image', 'title', 'date', 'live')
    list_filter = ('categories', 'tags', 'date', 'live')
    search_fields = ('title', 'intro', 'body')
    list_per_page = 10
    list_display_add_buttons = 'title'
    button_helper_class = MyButtonHelper
    inspect_view_enabled = False


# Now you just need to register your customised ModelAdmin class with Wagtail
modeladmin_register(MyBlogPageModelAdmin)
