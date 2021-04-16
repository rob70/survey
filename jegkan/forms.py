from django import forms

class EvaluateForm(forms.Form):
    evaluate = forms.IntegerField(
                        label='Evaluate', 
                        widget=forms.NumberInput(),
                        required=False
                        )


class AnswerForm(forms.Form):
    
    
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items(): 
            print ("%s : %s" %(key, value)) 
        
        
        
        
        # Super
        super().__init__(*args, **kwargs)
        
        
        
        GEEKS_CHOICES =( 
            ("0", "0"), 
            ("20", "20"), 
            ("50", "50"), 
            ("80", "80"), 
            ("100", "100"), 
        ) 
        print("Type of Geeks_choices: ", type(GEEKS_CHOICES))
        option_field = forms.ChoiceField(choices=GEEKS_CHOICES, widget=forms.RadioSelect, required=True)
        self.fields["option"] = option_field

class BaseAnswerFormSet(forms.BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["options"] = kwargs["options"][index]
        return kwargs
