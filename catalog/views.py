from django.shortcuts import render

def home(request):
    return render(request,  template_name='catalog/home.html')


def contacts(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Name: {name}, (Email: {phone}), Message: {message}')
    return render(request,  template_name='catalog/contacts.html')
