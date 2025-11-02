from django.shortcuts import render, redirect, get_object_or_404
from .forms import TicketForm
from .models import Ticket
from .classification import classify_input_data
import threading
from django.contrib.auth.decorators import login_required

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

@login_required
def ticket_dashboard(request):
    user = request.user

    # Superusers see all; departments see their own
    if user.is_superuser:
        tickets = Ticket.objects.all()
    elif user.groups.exists():
        department = user.groups.first().name
        tickets = Ticket.objects.filter(department=department)
    else:
        tickets = Ticket.objects.none()

    if request.method == 'POST':
        ticket_id = request.POST.get('ticket_id')
        new_status = request.POST.get('status')
        ticket = get_object_or_404(Ticket, id=ticket_id)
        ticket.status = new_status
        ticket.save()
        return redirect('ticket_dashboard')

    return render(request, 'dashboard.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    return render(request, 'ticket_detail.html', {'ticket': ticket})



def resolve_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.resolved = True
        ticket.resolution_comment = request.POST.get("resolution_comment", "")
        ticket.save()
    return redirect("ticket_detail", ticket_id=ticket.id)
