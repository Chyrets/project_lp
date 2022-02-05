from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views import View
from django.urls import reverse_lazy

from profiles.models import Profile
from .models import Follower


class FollowView(LoginRequiredMixin, View):
    """Отображение и отработка функционала подписки/отписки пользователя"""
    login_url = reverse_lazy('profile:login')

    def get(self, request, profile_slug, option):
        user = request.user

        try:
            sender = Profile.objects.get(user=user, used=True)
        except Profile.MultipleObjectsReturned:
            sender = Profile.objects.filter(user=user, used=True).first()

        profile = get_object_or_404(Profile, slug=profile_slug)

        if int(option):
            Follower.objects.get_or_create(recipient=profile, sender=sender)
        else:
            try:
                Follower.objects.get(recipient=profile, sender=sender).delete()
            except Follower.DoesNotExist:
                raise Http404
            except Follower.MultipleObjectsReturned:
                Follower.objects.filter(recipient=profile, sender=sender).delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
