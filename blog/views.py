# coding=utf8

from blog.models import Blog, Category
from django.http import Http404
from django.db.models import permalink
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import datetime

ARTICLES_PER_PAGE = 5


def index(request, page='1'):
    page = int(page)
    entryEnd = page * ARTICLES_PER_PAGE
    entryBegin = entryEnd - ARTICLES_PER_PAGE
    entryTotal = Blog.objects.count()
    if entryTotal < entryEnd:
        entryEnd = entryTotal
    if entryBegin > entryTotal:
        raise Http404

    totalPageNum = (entryTotal + ARTICLES_PER_PAGE - 1) / ARTICLES_PER_PAGE

    @permalink
    def get_absolute_url(page):
        return ("view_blog_page", None, {"page":page})

    return render_to_response('index.html', {
        'allCategories': Category.objects.all(),
        'nowDate': datetime.date.today(),
        'posts': Blog.objects.all()[entryBegin:entryEnd],
        'entryBegin': entryBegin + 1,
        'entryEnd': entryEnd,
        'entryTotal': entryTotal,

        'pagePrevious': get_absolute_url(page - 1) if page > 1 else None,
        'pageNext': get_absolute_url(page + 1) if page < totalPageNum else None,
    }, context_instance=RequestContext(request))


def view_post(request, slug):
    post = get_object_or_404(Blog, slug=slug)
    try:
        postPrevious = Blog.objects.reverse().filter(id__gt=post.id)[0]
    except IndexError:
        postPrevious = None

    try:
        postNext = Blog.objects.filter(id__gt=post.id)[0]
    except IndexError:
        postNext = None
    print post, postNext, postPrevious
    return render_to_response('view_post.html', {
        'allCategories': Category.objects.all(),
        'post': post,
        'categories': Category.objects.filter(blog=post),

        'noNeedDash': True,
        'entryEnd': Blog.objects.filter(id__gt=post.id).count() + 1,
        'entryTotal': Blog.objects.count(),

        'pagePrevious': postPrevious.get_absolute_url() if postPrevious else None,
        'pageNext': postNext.get_absolute_url() if postNext else None,
    }, context_instance=RequestContext(request))


def view_category(request, slug, page='1'):
    page = int(page)
    category = get_object_or_404(Category, slug=slug)
    blogsFromCategory = Blog.objects.filter(category=category)

    entryEnd = int(page) * ARTICLES_PER_PAGE
    entryBegin = entryEnd - ARTICLES_PER_PAGE
    entryTotal = blogsFromCategory.count()
    if entryTotal < entryEnd:
        entryEnd = entryTotal

    if entryBegin > entryTotal:
        raise Http404

    totalPageNum = (entryTotal + ARTICLES_PER_PAGE - 1) / ARTICLES_PER_PAGE

    @permalink
    def get_absolute_url(slug, page):
        return ("view_blog_category_page", None, {'slug': slug, 'page':page})

    return render_to_response('view_category.html', {
        'allCategories': Category.objects.all(),
        'category': category,
        'posts': blogsFromCategory[entryBegin:entryEnd],

        'entryBegin': entryBegin + 1,
        'entryEnd': entryEnd,
        'entryTotal': entryTotal,

        'pagePrevious': get_absolute_url(slug, page-1) if page > 1 else None,
        'pageNext': get_absolute_url(slug, page+1) if page < totalPageNum else None,
    }, context_instance=RequestContext(request))


def about_me(request):
    return render_to_response("about_me.html", {
        'allCategories': Category.objects.all(),
    })
