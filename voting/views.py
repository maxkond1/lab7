from django.views import generic
from .models import Poll, Option, Vote
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.db import IntegrityError
from django.http import HttpResponseForbidden
from django.core.cache import cache
from django.http import HttpResponse, HttpRequest
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

def custom_404_view(request: HttpRequest, exception) -> HttpResponse:
    return render(request, "errors/404.html", status=404)


class PollListView(generic.ListView):
    model = Poll
    template_name = 'poll_list.html'
    context_object_name = 'polls'

    def get_queryset(self):
        qs = Poll.objects.filter(is_active=True).order_by('-created_at')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(title__icontains=q)
        return qs

class PollDetailView(generic.DetailView):
    model = Poll
    template_name = 'poll_detail.html'
    context_object_name = 'poll'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        option_id = request.POST.get('option')
        option = get_object_or_404(Option, id=option_id, poll=self.object)
        user = request.user if request.user.is_authenticated else None
        ip = request.META.get('REMOTE_ADDR')
        # Prevent duplicate votes:
        # - for authenticated users, unique_together (user, option) triggers IntegrityError
        # - for guests (user is None), prevent multiple votes from same IP for this poll
        if user is None:
            if ip and Vote.objects.filter(option__poll=self.object, ip_address=ip).exists():
                return HttpResponseForbidden('Guest already voted from this IP')
        # Rate-limit: allow at most 10 votes per IP per minute (prevents flooding)
        if ip:
            key = f"votes_ip_{ip}"
            count = cache.get(key, 0)
            if count >= 10:
                return HttpResponse('Too many requests', status=429)
            cache.set(key, count + 1, timeout=60)
        # Prevent authenticated users from voting more than once per poll
        if user is not None:
            if Vote.objects.filter(user=user, option__poll=self.object).exists():
                return HttpResponseForbidden('You already voted')
        try:
            Vote.objects.create(user=user, option=option, ip_address=ip)
        except IntegrityError:
            return HttpResponseForbidden('You already voted')
        return redirect(reverse('poll_detail', args=[self.object.id]))


def logout_view(request):
    logout(request)
    return redirect('poll_list')

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('poll_list')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('poll_list')
    else:
        form = AuthenticationForm(request)
    return render(request, 'login.html', {'form': form})
