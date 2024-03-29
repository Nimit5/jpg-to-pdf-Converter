import time

from django.shortcuts import render, redirect
from django.http import JsonResponse,FileResponse,Http404
from django.views import View

from .forms import PhotoForm
from .models import Photo
import os
import img2pdf


class BasicUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class ProgressBarUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/progress_bar_upload/index.html', {'photos': photos_list})

    def post(self, request):
        time.sleep(1)  # You don't need this line. This is just to delay the process so you can see the progress bar testing locally.
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


class DragAndDropUploadView(View):
    def get(self, request):
        photos_list = Photo.objects.all()
        return render(self.request, 'photos/drag_and_drop_upload/index.html', {'photos': photos_list})

    def post(self, request):
        form = PhotoForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def clear_database(request):
    for photo in Photo.objects.all():
        photo.file.delete()
        photo.delete()
    return redirect(request.POST.get('next'))

def conver(request):
    l = []
    for photo in Photo.objects.all():
        l.append(photo.file)

    print(l)
    if(len(l)==0):
        raise Http404()
    with open("media/output.pdf", "wb") as f:
        f.write(img2pdf.convert([i for i in l ]))
        try:
            return FileResponse(open('media/output.pdf', 'rb'), content_type='application/pdf')
        except FileNotFoundError:
            raise Http404()

def display(request):
    try:
        clear_database(request)
        render(request,'photos/output.html', FileResponse(open('output.pdf', 'rb'), content_type='application/pdf'))
    except FileNotFoundError:
        raise Http404()