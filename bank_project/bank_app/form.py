from django import forms
from .models import District, Branch


class Application_form(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    date_of_birth = forms.DateField(label='Date of Birth', widget=forms.DateInput(attrs={'type': 'date'}))
    age = forms.IntegerField(label='Age')
    gender_choices = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    gender = forms.ChoiceField(label='Gender', choices=gender_choices, widget=forms.RadioSelect)
    phone_number = forms.CharField(label='Phone Number', max_length=15)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', widget=forms.Textarea)
    district = forms.ModelChoiceField(queryset=District.objects.all(), label='District')
    # branch = forms.ModelChoiceField(queryset=Branch.objects.none())
    branch = forms.ChoiceField(choices=[], required=False, widget=forms.Select(attrs={'disabled': 'disabled'}))
    account_type = forms.ChoiceField(choices=[
        ('savings', 'Savings Account'),
        ('current', 'Current Account'),
        # Add more choices as needed
    ])
    materials_provided = forms.MultipleChoiceField(
        choices=[
            ('debit_card', 'Debit Card'),
            ('credit_card', 'Credit Card'),
            ('cheque_book', 'Cheque Book'),
            # Add more choices as needed
        ],
        widget=forms.CheckboxSelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(Application_form, self).__init__(*args, **kwargs)
        self.fields['branch'].choices = [('', '---------')]

    def update_branch_choices(self, dist_id):
        if dist_id:
            branches = Branch.objects.filter(dist_id=dist_id)
            self.fields['branch'].choices = [(branch.id, branch.name) for branch in branches]
        else:
            self.fields['branch'].choices = [('', '---------')]
