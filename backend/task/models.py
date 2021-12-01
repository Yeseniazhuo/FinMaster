from django.db import models
from django.forms import ModelForm, DateInput
from django.urls import reverse
from login.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    due = models.DateTimeField()
    complete_status = models.BooleanField(default=False)

    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    @property
    def get_html_url(self):
        url = reverse('task_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


class TaskForm(ModelForm):
    class Meta:
        model = Task
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'due': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['title','content','due','complete_status']

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        # input_formats to parse HTML5 datetime-local input to datetime field
        self.fields['due'].input_formats = ('%Y-%m-%dT%H:%M',)
