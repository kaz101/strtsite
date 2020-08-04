from django import forms

class Transcript_url(forms.Form):
    url = forms.CharField()
class Check_box(forms.Form):

    actors_words = 0
    actor = ''
    character = ''
    words = 0
    box = forms.BooleanField()
class actor_obj(forms.Form):
    name = ''
    words = 0
    characters = []
    picture = ''
    percentage = 0
    select_char = forms.MultipleChoiceField(choices=[['a','hjgjhgjhgjhgj']])
    def reload(self):
        select_char = forms.MultipleChoiceField(choices=[['a','lkjlkjlkjlkj']])
