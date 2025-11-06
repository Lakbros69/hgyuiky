from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, TournamentParticipant, PaymentRequest, Order, SliderImage, WithdrawalRequest, ChatMessage


class UserRegistrationForm(forms.ModelForm):
    """User registration form"""
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    referral_code = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Referral Code (Optional)'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match!")
        
        return cleaned_data


class UserLoginForm(forms.Form):
    """User login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class ProfileUpdateForm(forms.ModelForm):
    """Profile update form"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class TournamentJoinForm(forms.ModelForm):
    """Tournament join form"""
    class Meta:
        model = TournamentParticipant
        fields = ['in_game_name', 'in_game_id']
        widgets = {
            'in_game_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your In-Game Name'
            }),
            'in_game_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your In-Game ID'
            }),
        }


class PaymentRequestForm(forms.ModelForm):
    """Payment request form"""
    class Meta:
        model = PaymentRequest
        fields = ['coins_amount', 'payment_amount', 'payment_screenshot', 'transaction_id']
        widgets = {
            'coins_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Number of Coins'
            }),
            'payment_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount Paid (Rs.)',
                'step': '0.01'
            }),
            'payment_screenshot': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'transaction_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Transaction ID (if available)'
            }),
        }


class OrderForm(forms.ModelForm):
    """Order form"""
    class Meta:
        model = Order
        fields = ['in_game_id', 'in_game_name']
        widgets = {
            'in_game_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your In-Game ID',
                'required': True
            }),
            'in_game_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your In-Game Name'
            }),
        }


class SliderImageForm(forms.ModelForm):
    """Form for managing homepage slider images"""

    class Meta:
        model = SliderImage
        fields = ['id', 'position', 'title', 'subtitle', 'image', 'button_text', 'button_url', 'is_active']
        widgets = {
            'position': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Slide title (optional)'
            }),
            'subtitle': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 2,
                'placeholder': 'Subtitle or description (optional)'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
            'button_text': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Button text (optional)'
            }),
            'button_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'https://your-link.example'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'toggle-input'
            }),
        }


class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'payment_qr', 'payment_method', 'account_details']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount to withdraw',
                'min': '1'
            }),
            'payment_qr': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'payment_method': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., eSewa, Khalti, Bank Account'
            }),
            'account_details': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your account details (account number, name, etc.)'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if self.user and amount > self.user.coins:
            raise forms.ValidationError(f'Insufficient balance. You have {self.user.coins} points.')
        if amount < 10:
            raise forms.ValidationError('Minimum withdrawal amount is 10 points.')
        return amount


class ChatMessageForm(forms.ModelForm):
    """Chat message form for users"""
    class Meta:
        model = ChatMessage
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Subject (optional)',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Type your message here...',
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False
