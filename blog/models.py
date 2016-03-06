# coding=utf8

from __future__ import unicode_literals

from django.db import models
from django.db.models import permalink
from django.template.defaultfilters import slugify
from django.utils.http import urlquote
import markdown


class Blog(models.Model):
    title = models.CharField(max_length=100)
    # slug用于生成有效的URL
    slug = models.SlugField(max_length=100, unique=True)
    body_markdown = models.TextField('Entry body', help_text='Use Markdown syntax.')
    body = models.TextField()
    posted = models.DateTimeField(db_index=True, auto_now_add=True)
    category = models.ManyToManyField("blog.Category", null=True)

    class Meta:
        ordering = ['-id']  # or '-posted'

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_post", None, {"slug":self.slug})

    def save(self):
        if not self.slug:
            self.slug = unicode(self.title)
        self.slug = slugify(urlquote(self.slug))

        if self.body_markdown:
            # markdown将txt文本转换为html格式
            self.body = markdown.markdown(self.body_markdown)
        super(Blog, self).save()


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    def __unicode__(self):
        return u'%s' % self.title

    @permalink
    def get_absolute_url(self):
        return ("view_blog_category", None, {"slug": self.slug})

    def save(self):
        if not self.slug:
            self.slug = unicode(self.title)
        self.slug = slugify(urlquote(self.slug))
        super(Category, self).save()
