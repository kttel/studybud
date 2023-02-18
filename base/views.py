from django.shortcuts import redirect

from django.contrib.auth import (
    get_user_model,
    views as login_views,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from base import models, forms, utils, mixins


class LoginUserView(login_views.LoginView):
    template_name = 'base/login_register.html'
    success_url = reverse_lazy('home')
    form_class = forms.UserLoginForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'login'
        return context


class RegisterUserView(generic.CreateView):
    form_class = forms.UserRegisterForm
    template_name = 'base/login_register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 'register'
        return context


class HomeView(generic.TemplateView):
    template_name = 'base/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = utils.update_home_context(context, self.request)
        return context


class RoomDetailView(generic.DetailView):
    model = models.Room
    template_name = 'base/room.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        room = models.Room.objects.get(pk=self.kwargs.get('pk'))
        context['room_messages'] = room.message_set.all()
        context['participants'] = room.participants.all()
        return context


class MessageView(LoginRequiredMixin, generic.View):
    def post(self, request, *args, **kwargs):
        utils.post_message(self.kwargs.get('pk'), self.request)
        return redirect('room', self.kwargs.get('pk'))


class ProfileView(generic.DetailView):
    model = get_user_model()
    template_name = 'base/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return utils.update_profile_context(context)


class CreateRoomView(mixins.RoomFormMixin, LoginRequiredMixin,
                     generic.FormView):
    form_class = forms.RoomForm
    template_name = 'base/room_form.html'
    success_url = reverse_lazy('home')


class UpdateRoomView(mixins.RoomFormMixin, LoginRequiredMixin,
                     generic.UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    template_name = 'base/room_form.html'

    def get_success_url(self):
        return reverse_lazy('room', kwargs={'pk': self.kwargs.get('pk')})


class DeleteRoomView(LoginRequiredMixin, generic.DeleteView):
    model = models.Room
    template_name = 'base/delete.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('home')


class DeleteMessageView(LoginRequiredMixin, generic.DeleteView):
    model = models.Message
    template_name = 'base/delete.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('room', kwargs={'pk': self.kwargs.get('pk_room')})


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = forms.UserForm
    template_name = 'base/edit-user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user-profile',
                            kwargs={'pk': self.request.user.pk})


class TopicsView(generic.ListView):
    model = models.Topic
    template_name = 'base/topics.html'
    context_object_name = 'topics'
    paginate_by = 3


class ActivityView(generic.ListView):
    model = models.Message
    template_name = 'base/activity.html'
    context_object_name = 'room_messages'
    paginate_by = 3
