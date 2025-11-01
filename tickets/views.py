from django.shortcuts import render, redirect
from .forms import TicketForm

def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = TicketForm()
    return render(request, 'index.html', {'form': form})

def success(request):
    return render(request, 'success.html')
