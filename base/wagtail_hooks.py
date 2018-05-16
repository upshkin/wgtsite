from django.http import HttpResponse
from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe

from wagtail.core import hooks
from wagtail.admin.site_summary import SummaryItem
from wagtail.admin.menu import MenuItem

from wagtail.admin import widgets as wagtailadmin_widgets


class MyWelcomePanel:
    order = 50

    def render(self):
        return mark_safe("""
            <section class="panel summary nice-padding">
              <p>WelcomePanel : @hooks.register('construct_homepage_panels')</p>
            </section>
            """)


class MySummaryItem(SummaryItem):
    name = 'Fake items'
    order = 400
    template = 'base/my_site_summary_item.html'

    def get_context(self):
        return {
            'single_site': True,
            'root_page': None,
            'total_pages': 100,
            'name': self.name,
        }


@hooks.register('construct_homepage_panels')
def add_another_welcome_panel(_, panels):
    return panels.append(MyWelcomePanel())


@hooks.register('construct_homepage_summary_items')
def add_homepage_summary_items(request, items):
    return items.append(MySummaryItem(request))


@hooks.register('construct_main_menu')
def hide_explorer_menu_item_from_frank(_, menu_items):
    menu_items.append(MenuItem(
        label='Hooked item',
        url='#',
        order=10000,
        classnames='icon icon-spinner',
    ))


@hooks.register('register_admin_menu_item')
def register_frank_menu_item():
    return MenuItem(
        'Another one',
        reverse('amorphus'),
        classnames='icon icon-spinner',
        order=10001
    )


def admin_view(request):
    return HttpResponse(
        "I have hooked into admin menu and set a link to my page",
        content_type="text/plain")


@hooks.register('register_admin_urls')
def urlconf_time():
    return [
        url(r'^amorphus/test/$', admin_view, name='amorphus'),
    ]


@hooks.register('register_page_listing_buttons')
def page_listing_buttons(page, page_perms, is_parent=False):
    yield wagtailadmin_widgets.PageListingButton(
        page.title,
        page.url,
        priority=1
    )


@hooks.register('register_page_listing_more_buttons')
def page_listing_more_buttons(page, page_perms, is_parent=False):
    yield wagtailadmin_widgets.Button(
        'Полный урл',
        page.full_url,
        priority=1
    )