from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .forms import TicketForm


@login_required
def home(request):
    return render(request, "managelitreview/home.html")


def _response_new_update_ticket(request, form, type_):
    if request.method == "POST":
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("managelitreview:home")

    return render(request, "managelitreview/create_ticket.html", {"form": form})


@login_required
def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect("managelitreview:display_ticket", ticket.id)
    else:
        form = TicketForm()
    return render(request, "managelitreview/create_ticket.html", {"form": form})


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("managelitreview:display_ticket", ticket_id)

    return render(request, "managelitreview/create_ticket.html", {"form": form})


@login_required
def display_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)

    return render(request, "managelitreview/display_ticket.html", {"ticket": ticket})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket.delete()
    return redirect("managelitreview:home")