from itertools import chain

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import OuterRef, Exists, Value

from django.shortcuts import render, redirect, get_object_or_404

from . import models
from .forms import TicketForm, ReviewForm

NUMBER_POST_PER_PAGE = 3


def allowed_to_access_the_post(type_class):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = args[0]
            all_users = set(request.user.all_users)
            post_all_users = {}
            print(all_users)
            if type_class == models.Ticket:
                ticket = models.Ticket.objects.get(id=kwargs["ticket_id"])
                post_all_users = set(ticket.all_users)
            elif type_class == models.Review:
                review = models.Review.objects.get(id=kwargs["review_id"])
                post_all_users = set(review.ticket.all_users)
            if len(post_all_users & all_users) == 0:
                raise PermissionDenied
            return func(*args, **kwargs)

        return wrapper

    return decorator


@login_required
def home(request):
    followed_users = [f.followed_user for f in request.user.following.all()]
    followed_users.append(request.user)
    review_by_actif_user = models.Review.objects.filter(
        ticket=OuterRef("pk"), user=request.user
    )
    tickets = (
        models.Ticket.objects.filter(user__in=followed_users)
        .annotate(post_type=Value("TICKET"))
        .annotate(review_by_actif_user=Exists(review_by_actif_user))
    )

    reviews = models.Review.objects.filter(user__in=followed_users).annotate(
        post_type=Value("REVIEW")
    )
    posts = chain(reviews, tickets)
    posts_sorted_datetime = sorted(
        posts, key=lambda post: post.time_created, reverse=True
    )
    posts = sorted(posts_sorted_datetime, key=lambda post: post.post_type)
    paginator = Paginator(posts, NUMBER_POST_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "update_authorized": False}
    return render(
        request,
        "managelitreview/home.html",
        context=context,
    )


@login_required
def display_my_posts(request):
    review_by_actif_user = models.Review.objects.filter(
        ticket=OuterRef("pk"), user=request.user
    )
    tickets = (
        models.Ticket.objects.filter(user=request.user)
        .annotate(post_type=Value("TICKET"))
        .annotate(review_by_actif_user=Exists(review_by_actif_user))
    )
    reviews = models.Review.objects.filter(user=request.user).annotate(
        post_type=Value("REVIEW")
    )
    posts = chain(reviews, tickets)
    posts_sorted_datetime = sorted(
        posts, key=lambda post: post.time_created, reverse=True
    )
    posts = sorted(posts_sorted_datetime, key=lambda post: post.post_type)
    paginator = Paginator(posts, NUMBER_POST_PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "update_authorized": True}
    return render(
        request,
        "managelitreview/posts.html",
        context=context,
    )


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
@allowed_to_access_the_post(models.Ticket)
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
@allowed_to_access_the_post(models.Ticket)
def display_ticket(request, ticket_id):
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, "managelitreview/display_ticket.html", {"ticket": ticket})


@login_required
@allowed_to_access_the_post(models.Ticket)
def delete_ticket(request, ticket_id):
    print('request.meth', request.method)
    if request.method == "DELETE":
        print('ca marche!!!')
        ticket = get_object_or_404(models.Ticket, id=ticket_id)
        ticket.delete()
    return redirect("managelitreview:display_my_tickets")


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
@allowed_to_access_the_post(models.Review)
def delete_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    review.delete()
    return redirect("managelitreview:display_my_tickets")


@login_required
def update_review_with_ticket(request, review):

    ticket = review.ticket
    review_form = ReviewForm(instance=review)
    ticket_form = TicketForm(instance=ticket)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        ticket_form = TicketForm(request.POST, request.FILES, instance=ticket)
        if ticket_form.is_valid() & review_form.is_valid():
            ticket_form.save()
            review_form.save()
            return redirect("managelitreview:display_review", review.id)
    return render(
        request,
        "managelitreview/form_review_with_ticket.html",
        {"review_form": review_form, "ticket_form": ticket_form, "review": review},
    )


@login_required
@allowed_to_access_the_post(models.Review)
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


@login_required
def update_review_without_ticket(request, review):

    review_form = ReviewForm(instance=review)
    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=review)
        if review_form.is_valid():
            review_form.save()
            return redirect("managelitreview:display_review", review.id)
    return render(
        request,
        "managelitreview/form_review.html",
        {"review_form": review_form, "review": review},
    )


@login_required
@allowed_to_access_the_post(models.Review)
def update_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    if review.user == review.ticket.user:
        return update_review_with_ticket(request, review)
    else:
        return update_review_without_ticket(request, review)
