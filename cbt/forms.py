from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from cbt.models import (Answer, Question, Student, StudentAnswer,
                              Subject, User, Details, Department)


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class StudentSignUpForm(UserCreationForm):
    
    department = forms.ModelMultipleChoiceField(
        queryset=Department.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'radio_1'}),
        required=True
    )


        #matric = forms.ChoiceField(required=True, widget=forms.RadioSelect(attrs={'class': 'radio_1'}))

    matric = forms.CharField(required=True, widget=forms.TextInput(attrs={'required': "required"}))
    
    

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','matric',)
       

       

   
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.department.add(*self.cleaned_data.get('department'))
        return user

  
class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }
        


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )

class ExamForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')



class CourseDetailsForm(forms.ModelForm):
    class Meta:
        model = Details
        fields = ('semester',  'maximum_marks', 'duration', 'total_marks', 'no_of_question', 'instructions')

        
