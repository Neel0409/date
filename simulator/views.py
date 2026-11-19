from django.shortcuts import render, redirect
from .forms import DateSelectionForm


def home(request):
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = DateSelectionForm()
    return render(request, 'simulator/home.html', {'form': form})


def success(request):
    return render(request, 'simulator/success.html')
