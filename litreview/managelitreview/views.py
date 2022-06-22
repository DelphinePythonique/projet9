from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef, Exists

from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .forms import TicketForm, ReviewForm


@login_required
def home(request):
    followed_users = [f.followed_user for f in request.user.following.all()]
    followed_users.append(request.user)
    review_by_actif_user = models.Review.objects.filter(
        ticket=OuterRef('pk'),
        user=request.user
    )
    tickets = models.Ticket.objects.filter(user__in=followed_users).annotate(review_by_actif_user=Exists(review_by_actif_user))
    ticket_with_type = [{"type": "ticket", "item": ticket} for ticket in tickets]
    reviews = models.Review.objects.filter(user__in=followed_users)
    review_with_type = [{"type": "review", "item": review} for review in reviews]
    posts = ticket_with_type + review_with_type
    posts_sorted_datetime = sorted(posts, key=lambda post: post["item"].time_created, reverse=True)
    posts = sorted(posts_sorted_datetime, key=lambda post: post["type"])

    return render(request, "managelitreview/home.html", context={"posts": posts,
                                                                 'update_authorized': False})


@login_required
def display_my_posts(request):

    tickets = models.Ticket.objects.filter(user=request.user)
    ticket_with_type = [{"type": "ticket", "item": ticket} for ticket in tickets]
    reviews = models.Review.objects.filter(user=request.user)
    review_with_type = [{"type": "review", "item": review} for review in reviews]

    posts = ticket_with_type + review_with_type
    posts_sorted_datetime = sorted(posts, key=lambda post: post["item"].time_created, reverse=True)
    posts = sorted(posts_sorted_datetime, key=lambda post: post["type"])
    return render(request, "managelitreview/posts.html", context={
        "posts": posts,
        'update_authorized': True
    })


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
def create_review_with_ticket(request):
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
    return render(
        request,
        "managelitreview/form_review_with_ticket.html",
        {"ticket_form": ticket_form, "review_form": review_form},
    )


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    review.delete()
    return redirect("managelitreview:home")


@login_required
def update_review_with_ticket(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    ticket = review.ticket
    review_form = ReviewForm(instance=review)
    ticket_form = TicketForm(instance=ticket)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid() & review_form.is_valid():
            ticket_form.save()
            review_form.save()
            return redirect("managelitreview:display_review", review_id)

    return render(
        request,
        "managelitreview/form_review_with_ticket.html",
        {"review_form": review_form, "ticket_form": ticket_form, "review": review},
    )

@login_required
def display_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, "managelitreview/display_review.html", {"review": review})


@login_required
def create_review(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("managelitreview:display_ticket", ticket.id)
    else:
        review_form = ReviewForm()
    return render(
        request,
        "managelitreview/form_review.html",
        {"ticket": ticket, "review_form": review_form},
    )
