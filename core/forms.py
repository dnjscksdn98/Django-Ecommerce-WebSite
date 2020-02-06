from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address',
        'placeholder': '1234 Main St',
        'autocomplete': 'off'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'address-2',
        'placeholder': 'Apartment or suite',
        'autocomplete': 'off'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'custom-select d-block w-100'
        })
    )
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zip',
        'autocomplete': 'off'
    }))

    same_shipping_address = forms.BooleanField(
        required=False, widget=forms.CheckboxInput()
    )
    save_info = forms.BooleanField(
        required=False, widget=forms.CheckboxInput()
    )

    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(),
        choices=PAYMENT_CHOICES
    )  # only one select is possible


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo Code',
        'aria-label': "Recipient's username",
        'aria-describedby': 'basic-addon2',
        'autocomplete': 'off'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField(widget=forms.TextInput(attrs={
        'autocomplete': 'off',
        'class': 'form-control',
        'id': 'form106'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
        'class': 'md-textarea form-control',
        'id': 'form107'
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'autocomplete': 'off',
        'class': 'form-control',
        'id': 'form105'
    }))
