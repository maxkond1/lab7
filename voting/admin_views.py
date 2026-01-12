from django import forms
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render
import openpyxl
from django.http import HttpResponseBadRequest
import datetime

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
    # If a table is selected and fields param provided (comma-separated), perform export
    if request.method == 'GET' and request.GET.get('action') == 'download':
        table = request.GET.get('table')
        # Accept multiple checkbox values (GET list) or comma-separated single value
        fields = request.GET.getlist('fields')
        if len(fields) == 1 and ',' in fields[0]:
            fields = [f.strip() for f in fields[0].split(',') if f.strip()]
        wb = openpyxl.Workbook()
        ws = wb.active
        # Resolve model by table parameter
        if table == 'poll':
            from .models import Poll as Model
        elif table == 'option':
            from .models import Option as Model
        else:
            from .models import Vote as Model

        allowed = [f.name for f in Model._meta.fields]
        invalid = [f for f in fields if f not in allowed]
        if invalid:
            return HttpResponseBadRequest(f"Invalid fields requested: {', '.join(invalid)}")

        ws.append(fields)
        qs = Model.objects.all().values_list(*fields)
        for row in qs:
            processed = []
            for val in row:
                # openpyxl does not accept timezone-aware datetimes/times
                if isinstance(val, datetime.datetime) and val.tzinfo is not None:
                    val = val.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                if isinstance(val, datetime.time) and val.tzinfo is not None:
                    val = val.astimezone(datetime.timezone.utc).replace(tzinfo=None)
                processed.append(val)
            ws.append(processed)
        resp = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        resp['Content-Disposition'] = 'attachment; filename=export.xlsx'
        wb.save(resp)
        return resp

    # Render form with selectable fields for chosen table
    table = request.GET.get('table')
    allowed = []
    if table:
        if table == 'poll':
            from .models import Poll as Model
        elif table == 'option':
            from .models import Option as Model
        else:
            from .models import Vote as Model
        allowed = [f.name for f in Model._meta.fields]
    form = ExportForm(request.GET or None)
    return render(request, 'admin/export_form.html', {'form': form, 'allowed': allowed, 'selected_table': table})
