from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .models import Stream
import subprocess

class StreamAdmin(admin.ModelAdmin):
    change_list_template = "admin/stream_changelist.html"
    change_form_template = "admin/stream_change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('start_stream/<int:stream_id>/', self.admin_site.admin_view(self.start_stream), name='start-stream'),
            path('stop_stream/<int:stream_id>/', self.admin_site.admin_view(self.stop_stream), name='stop-stream'),
        ]
        return custom_urls + urls

    def start_stream(self, request, stream_id):
        stream = get_object_or_404(Stream, id=stream_id)
        command = [
            'ffmpeg',
            '-i', stream.source_url,
            '-f', 'rtsp',
            '-rtsp_transport', 'tcp',
            stream.destination_url
        ]
        subprocess.Popen(command)
        self.message_user(request, "Stream started.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def stop_stream(self, request, stream_id):
        # Реализуйте логику остановки потока, если необходимо
        self.message_user(request, "Stream stopped.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['start_stream_url'] = f'start_stream/{object_id}/'
        extra_context['stop_stream_url'] = f'stop_stream/{object_id}/'
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

admin.site.register(Stream, StreamAdmin)