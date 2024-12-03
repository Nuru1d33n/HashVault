from django import forms
from .models import Password, PasswordHash

class PasswordForm(forms.Form):
    CHOICES = [
        ('input', 'Enter password manually'),
        ('textarea', 'Enter passwords in textarea'),
        ('file', 'Upload a file')
    ]

    choice = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)
    password_input = forms.CharField(max_length=4444, required=False)
    password_text_area = forms.CharField(widget=forms.Textarea, required=False)
    password_file = forms.FileField(required=False)

    def save(self):
        """
        Save the password and create associated hashes.
        """
        # Based on user choice, determine how to get the password
        if self.cleaned_data['choice'] == 'input':
            password = self.cleaned_data['password_input']
        elif self.cleaned_data['choice'] == 'textarea':
            password = self.cleaned_data['password_text_area']
        else:  # file upload
            # Assuming only one password is stored per file for simplicity
            file = self.cleaned_data['password_file']
            password = file.read().decode('utf-8')

        # Create a new Password instance and save
        password_instance = Password(value=password)
        password_instance.save()
        return password_instance

class HashForm(forms.Form):
    HASH_CHOICES = [
        ('md5', 'MD5'),
        ('sha1', 'SHA-1'),
        ('sha224', 'SHA-224'),
        ('sha256', 'SHA-256'),
        ('sha384', 'SHA-384'),
        ('sha512', 'SHA-512'),
        ('sha3_256', 'SHA-3-256')
    ]

    hash_type = forms.ChoiceField(choices=HASH_CHOICES)
    password = forms.CharField(max_length=4444)

    def clean_password(self):
        """
        Validates password and creates the corresponding hash.
        """
        password_value = self.cleaned_data['password']
        password_instance = Password(value=password_value)
        password_instance.save()
        
        # Find the hash of the requested type
        hash_type = self.cleaned_data['hash_type']
        password_hash = PasswordHash.objects.filter(
            original_password=password_instance,
            hash_type=hash_type
        ).first()
        
        if password_hash:
            return password_hash.value
        raise forms.ValidationError("Hash creation failed.")


class HashCheckForm(forms.Form):
    """
    Form for checking if a hash exists in the database.
    """
    hash_value = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the hash value here...'
        }),
        label='Hash Value'
    )

    def clean_hash_value(self):
        """
        Custom validation for hash_value to ensure it is not empty or invalid.
        """
        hash_value = self.cleaned_data.get('hash_value', '').strip()
        
        if not hash_value:
            raise forms.ValidationError("Hash value cannot be empty.")
        
        # Optionally, validate the hash format (e.g., length, alphanumeric, etc.)
        if not hash_value.isalnum():
            raise forms.ValidationError("Hash value must be alphanumeric.")
        
        return hash_value



class HashIdentifyForm(forms.Form):
    hash_value = forms.CharField(max_length=128)

    def clean(self):
        hash_value = self.cleaned_data['hash_value']
        detected_hash_type = Password.detect_hash_type(hash_value)
        if detected_hash_type == 'Unknown':
            raise forms.ValidationError("Unable to detect hash type.")
        self.cleaned_data['detected_hash_type'] = detected_hash_type
        return self.cleaned_data

class IdentifyHashForm(forms.Form):
    hash_value = forms.CharField(label='Enter the hash', max_length=128)
    
    def clean(self):
        hash_value = self.cleaned_data['hash_value']
        detected_hash_type = Password.detect_hash_type(hash_value)
        if detected_hash_type == 'Unknown':
            raise forms.ValidationError("Unable to detect hash type.")
        self.cleaned_data['detected_hash_type'] = detected_hash_type
        return self.cleaned_data
