from django import forms


class IdCarverForm(forms.Form):
    text = forms.CharField(label='Enter your text', widget=forms.Textarea)
    no_exceptions = forms.BooleanField(label='No exceptions', required=False, initial=False)


class IdGeneratorForm(forms.Form):
    number_of_ids = forms.IntegerField(label='Number of codes to generate')
    no_exceptions = forms.BooleanField(label='No exceptions', required=False, initial=False)
