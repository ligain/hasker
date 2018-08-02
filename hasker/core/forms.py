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
        return tags


class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('text', )
