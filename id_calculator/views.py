from django.shortcuts import render
from django.contrib import messages
from .forms import IdCarverForm, IdGeneratorForm
from .personal_id_tools.lithuanian_personal_ID_tools import LithuanianIDTools as lpid
from .personal_id_tools.id_information import text_sanitizer


def detect_ids(request):
    # Define context values:
    context = {
        'title': 'Personal ID carver',
        'form_name': 'Find Personal Lithuanian IDs',
        'method': 'post',
        'button_name': 'Find IDs',
        'form': IdCarverForm()
    }
    if request.method == 'POST':
        form = IdCarverForm(request.POST)
        if form.is_valid():
            exceptions = bool(request.POST.get('no_exceptions', False))
            results = text_sanitizer(request.POST['text'], exceptions)
            # Update context w/ form data if form is submitted:
            context.update({
                'form': form,
                'results': results
            })

            if all(len(value) == 0 for value in results.values()):
                messages.add_message(request, messages.WARNING,
                                     'No strings resembling personal or corporate IDs were found')

    return render(request, 'id_carver.html', context=context)


def personal_id_data(request, personal_id):
    return render(request, 'personal_data_viewer.html',
                  context={'data': lpid.get_personal_description(personal_id)})


def generate_ids(request):
    # Define context values:
    context = {
        'title': 'Personal ID generator',
        'form_name': 'Generate Personal Lithuanian IDs',
        'button_name': 'Generate IDs',
        'form': IdGeneratorForm()
    }
    if request.method == 'GET':
        form = IdGeneratorForm(request.GET)
        if form.is_valid():
            exceptions = bool(request.GET.get('no_exceptions', False))
            results = [lpid.personal_id_generator(exceptions) for foo in range(int(request.GET['number_of_ids']))]
            # Update context w/ form data if form is submitted:
            context.update({
                'form': form,
                'results': results
            })
    return render(request, 'id_generator.html', context=context)
