from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Password, PasswordHash
from .forms import PasswordForm, HashForm, HashCheckForm, HashIdentifyForm

import hashlib


def index(request):
    """
    Home page that handles the display of forms and actions.
    """
    return render(request, 'index.html')


def handle_password(request):
    """
    Handle password input, either manually, from textarea, or file upload.
    Reads the input line by line (or word by word) and saves only non-duplicate entries.
    """
    if request.method == 'POST':
        form = PasswordForm(request.POST, request.FILES)
        if form.is_valid():
            choice = form.cleaned_data['choice']
            password = None

            # Case for textarea input
            if choice == 'textarea':
                password_text = form.cleaned_data['password_text_area']
                password_lines = password_text.splitlines()  # Split by lines

                for line in password_lines:
                    if line and not Password.objects.filter(value=line).exists():
                        password_obj = Password(value=line)
                        password_obj.save()
                        messages.success(request, f'Password "{line}" has been successfully saved.')
                    else:
                        messages.error(request, f'Password "{line}" already exists in the database.')

            # Case for file upload
            elif choice == 'file':
                uploaded_file = request.FILES['password_file']
                file_content = uploaded_file.read()  # Read and decode file content
                # file_content = uploaded_file.read().decode('utf-8')  # Read and decode file content
                password_lines = file_content.splitlines()  # Split by lines

                for line in password_lines:
                    if line and not Password.objects.filter(value=line).exists():
                        password_obj = Password(value=line)
                        password_obj.save()
                        messages.success(request, f'Password "{line}" from file has been successfully saved.')
                    else:
                        messages.error(request, f'Password "{line}" from file already exists in the database.')

            # Case for manual input (single password input)
            elif choice == 'input':
                password = form.cleaned_data['password_input']
                if password and not Password.objects.filter(value=password).exists():
                    password_obj = Password(value=password)
                    print(password)
                    # print(password_obj.pk)
                    password_obj.save()
                    messages.success(request, f'Password "{password}" has been successfully saved.')
                else:
                    messages.error(request, f'Password "{password}" already exists in the database.')

            # Redirect to the same page after processing
            return redirect('handle_password')

    else:
        form = PasswordForm()

    return render(request, 'password_form.html', {'form': form})


def hash_password(request, password_id):
    """
    Generate and display password hashes for the given password.
    """
    password_obj = Password.objects.get(id=password_id)
    hashes = PasswordHash.objects.filter(original_password=password_obj)

    return render(request, 'hash_list.html', {'password': password_obj, 'hashes': hashes})

def check_hash(request):
    """
    Check if the hash exists in the database and is valid.
    """
    if request.method == 'POST':
        form = HashCheckForm(request.POST)
        if form.is_valid():
            hash_value = form.cleaned_data['hash_value']
            
            # Check if the hash value is empty
            if not hash_value.strip():
                messages.error(request, "Hash value cannot be empty.")
                return render(request, 'hash_check.html', {'form': form})
            
            try:
                # Try to get the hash object based on the hash_value
                hash_obj = PasswordHash.objects.get(hash_value=hash_value)  # Adjust field name as necessary
                
                # Check if the original password is available
                if hash_obj.password:
                    messages.success(request, f"Hash found: {hash_obj.algorithm}")
                    messages.success(request, f"Original password: {hash_obj.password.value}")
                else:
                    messages.error(request, "Original password not found.")
            
            except PasswordHash.DoesNotExist:
                messages.error(request, "Hash not found in the database.")
    
    else:
        form = HashCheckForm()

    return render(request, 'hash_check.html', {'form': form})
