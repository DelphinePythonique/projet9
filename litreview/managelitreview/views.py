from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .forms import TicketForm, ReviewForm


@login_required
def home(request):
    return render(request, "managelitreview/home.html")


@login_required
def display_my_tickets(request):
    tickets = models.Ticket.objects.filter(user=request.user)
    return render(request, "managelitreview/my_tickets.html",
                  context={'tickets': tickets})


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
    return render(request, "managelitreview/form_ticket.html", {"form": form})


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    form = TicketForm(instance=ticket)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect("managelitreview:display_ticket", ticket_id)

    return render(
        request, "managelitreview/form_ticket.html", {"form": form, "ticket": ticket}
    )


@login_required
def display_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, "managelitreview/display_ticket.html", {"ticket": ticket})


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    ticket.delete()
    return redirect("managelitreview:home")


@login_required
def create_review(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() & review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("managelitreview:display_ticket", ticket.id)
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, "managelitreview/form_review.html", {"ticket_form": ticket_form, "review_form": review_form})
