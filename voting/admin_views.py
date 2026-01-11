from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
import openpyxl

# Простая форма для выбора таблицы и полей для экспорта
class ExportForm(forms.Form):
    TABLE_CHOICES = (
        ('poll', 'Poll'),
        ('option', 'Option'),
        ('vote', 'Vote'),
    )
    table = forms.ChoiceField(choices=TABLE_CHOICES)
    fields = forms.CharField(help_text='Comma-separated field names')


@staff_member_required
def export_xlsx(request):
    """Admin-only view that exports selected model fields to an XLSX file.

    Query params / form:
    - table: 'poll'|'option'|'vote'
    - fields: comma separated names of fields to include
    """
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
        form = ExportForm(request.GET or None)
        return render(request, 'admin/export_form.html', {'form': form})
