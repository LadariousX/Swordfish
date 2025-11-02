from django.shortcuts import render, redirect
from .forms import TicketForm
from .models import Ticket
from .classification import classify_input_data
import threading

def process_ticket_async(ticket_id):
    def task():
        ticket = Ticket.objects.get(id=ticket_id)
        classify_input_data(ticket)
    threading.Thread(target=task, daemon=True).start()


def submit_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save()
            process_ticket_async(ticket.id) #save ticket then concurrent fill in the rest
            return redirect('success')
    else:
        form = TicketForm()
    return render(request, 'index.html', {'form': form})

def success(request):
    return render(request, 'success.html')
