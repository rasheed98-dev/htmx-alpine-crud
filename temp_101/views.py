from http.client import HTTPResponse
import json
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from temp_101.forms import BlogForm
from temp_101.models import Blog


def index(request):
    print(Blog.objects.all().values('id', 'title', 'description'))
    return render(request, 'temp_101/index.html', {
        'blogs': Blog.objects.all()
    })


def blog_create(request):
    blog_form = BlogForm(request.POST or None)
    if request.method == 'POST' and blog_form.is_valid():
        blog_form.save()
        messages.success(request, 'blog created successfully!')
        return redirect('index')

    return render(request, 'temp_101/blog_create.html', {
        'form': blog_form
    })


def blog_view(request, id):
    blog = Blog.objects.get(id=id)
    blog_form = BlogForm(request.POST or None, instance=blog)
    if request.method == 'POST' and blog_form.is_valid():
        blog_form.save()
        messages.success(request, 'blog updated successfully!')
        return redirect('index')

    return render(request, 'temp_101/blog_update.html', {
        'form': blog_form
    })


def blog_delete(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request, 'blog deleted successfully!')
    return redirect('index')


def blog_render(request, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'temp_101/partials/blog.html', {
        'blog': blog
    })


def blog_partial_create(request):
    title = request.POST.get('title')
    desc = request.POST.get('description')
    blog = Blog(
        title=title,
        description=desc
    )

    blog.save()
    return render(request, 'temp_101/partials/blog.html', {
        'blog': blog
    })


def blog_partial_aupdate(request, id):
    print(request.POST)
    blog = Blog.objects.get(id=id)
    title = request.POST.get('title')
    desc = request.POST.get('description')
    blog.title = title
    blog.description = desc
    blog.save()
    return render(request, 'temp_101/partials/blog.html', {
        'blog': blog
    })


def blog_partial_bupdate(request, id):
    blog = Blog.objects.get(id=id)
    return render(request, 'temp_101/partials/blog_update.html', {
        'blog': blog
    })


def blog_partial_delete(request, id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    return HttpResponse('')


def blog_partial_delete_all(request):
    inputs = request.POST.getlist('id')
    Blog.objects.filter(id__in=inputs).delete()
    response = HttpResponse('')
    response['HX-Redirect'] = reverse('index')
    return response


def blog_list(request):
    blogs = [{
        "id": blog.id,
        "title": blog.title,
        "description": blog.description
    } for blog in Blog.objects.all()]

    return JsonResponse(status=200, data=blogs, safe=False)
    # return JsonResponse({"key": "value"})

@csrf_exempt
def add_blog(request):
    data = json.loads(request.body)
    # print(data)
    blog = Blog.objects.create(
        title=data['title'],
        description=data['description']
    ).save()
    # blog.save()
    # print(JsonResponse(status=200, data=blog, safe=False))
    return JsonResponse(status=200, data=blog, safe=False)
    # print(blog)
@csrf_exempt
def delete_blog(request, blog_id):
    # blog = get_object_or_404(Blog, pk=blog_id)
    blog = Blog.objects.get(id=blog_id).delete()
    print(blog)
    # print(blog)
    # print(blog_id)
    # blog.delete()
    return JsonResponse(status=204, data={'message': 'task deleted'})