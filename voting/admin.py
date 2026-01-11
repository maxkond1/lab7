from django.contrib import admin
from .models import Poll, Option, Vote
from django.urls import path
from django import forms
from django.http import HttpResponse
import openpyxl

@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'poll', 'created_at')

@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'ip_address', 'created_at')

# Простая admin view для экспортов: выбираем таблицу и поля
class ExportForm(forms.Form):
    TABLE_CHOICES = (
        ('poll', 'Poll'),
        ('option', 'Option'),
        ('vote', 'Vote'),
    )
    table = forms.ChoiceField(choices=TABLE_CHOICES)
    fields = forms.CharField(help_text='Comma-separated field names')

class ExportAdminView(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path('export-xlsx/', self.admin_site.admin_view(self.export_xlsx), name='export-xlsx'),
        ]
        return custom + urls

    def export_xlsx(self, request):
        form = ExportForm(request.GET or None)
        if request.method == 'GET' and 'table' in request.GET:
            table = request.GET.get('table')
            fields = [f.strip() for f in request.GET.get('fields', '').split(',') if f.strip()]
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.append(fields)
            if table == 'poll':
                from .models import Poll
                qs = Poll.objects.all().values_list(*fields)
            elif table == 'option':
                from .models import Option
                qs = Option.objects.all().values_list(*fields)
            else:
                from .models import Vote
                qs = Vote.objects.all().values_list(*fields)
            for row in qs:
                ws.append(list(row))
            resp = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            resp['Content-Disposition'] = 'attachment; filename=export.xlsx'
            wb.save(resp)
            return resp
        else:
            from django.shortcuts import render
            return render(request, 'admin/export_form.html', {'form': form})

# регистрируем view на сайте админки
admin_site = admin.site
admin_site.get_urls = admin_site.get_urls
admin_site.registered_export = ExportAdminView()
