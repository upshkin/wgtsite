# New imports added for forms and ParentalManyToManyField
from django import forms
from django.db import models

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from wagtail.core.models import Page, Orderable
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.edit_handlers import FormSubmissionsPanel


class BlogPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['blog.BlogPost']

    def get_context(self, request):
        # Update context to include only published posts,
        # ordered by reverse-chron
        context = super().get_context(request)
        blogposts = self.get_children().live().order_by('-first_published_at')
        context['blogposts'] = blogposts
        return context


class BlogPostTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPost',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogTagPage(Page):
    subpage_types = []

    def get_context(self, request):
        # Filter by tag
        tag = request.GET.get('tag')
        blogposts = BlogPost.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['blogposts'] = blogposts
        return context


class BlogPost(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPostTag, blank=True)
    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading="Blog information", classname="collapsible"),
        FieldPanel('intro'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images"),
    ]

    subpage_types = []
    parent_page_types = ['blog.BlogPage']

    @property
    def thumb_image(self):
        thumb_img = self.gallery_images.first()
        if thumb_img:
            return thumb_img.image.get_rendition('fill-70x70').img_tag()
        else:
            return None


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(BlogPost, on_delete=models.CASCADE,
                       related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'blog categories'


@register_setting(icon='group')
class SocialMediaSettings(BaseSetting):
    facebook = models.URLField(
        help_text='Your Facebook page URL')
    instagram = models.CharField(
        max_length=255, help_text='Your Instagram username, without the @')
    trip_advisor = models.URLField(
        help_text='Your Trip Advisor page URL')
    youtube = models.URLField(
        help_text='Your YouTube channel or user account URL')

    class Meta:
        verbose_name = 'Social settings'


class FormField(AbstractFormField):
    page = ParentalKey(
        'FormPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class FormPage(AbstractEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname='full'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text', classname='full'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname='col6'),
                FieldPanel('to_address', classname='col6'),
            ]),
            FieldPanel('subject'),
        ], 'Email'),
    ]

    subpage_types = []


