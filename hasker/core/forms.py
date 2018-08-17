import re

from django import forms

from hasker.core.models import Question, Answer


class CreateQuestionForm(forms.ModelForm):
    tags = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Question
        fields = ('title', 'text', 'tags')

    def clean_tags(self):
        tags = self.cleaned_data['tags']
        if ',' not in tags:
            raise forms.ValidationError("Tags should be separated by comma.")
        invalid_symbols = re.search(r'[^-\w,\s]+', tags)
        if invalid_symbols:
            raise forms.ValidationError("Tags contain invalid symbol: {} "
                                        "They should contain letters, "
                                        "digits and - symbol".format(invalid_symbols.group(0)))
        return tags


class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', )


class QueryForm(forms.Form):
    q = forms.CharField(max_length=100)
