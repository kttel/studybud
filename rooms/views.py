from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from base import models

from rooms import forms, mixins, utils


class RoomDetailView(generic.DetailView):
    model = models.Room
    template_name = 'rooms/room.html'

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


class CreateRoomView(mixins.RoomFormMixin, LoginRequiredMixin,
                     generic.FormView):
    form_class = forms.RoomForm
    template_name = 'rooms/room_form.html'
    success_url = reverse_lazy('home')


class UpdateRoomView(mixins.RoomFormMixin, LoginRequiredMixin,
                     generic.UpdateView):
    model = models.Room
    form_class = forms.RoomForm
    template_name = 'rooms/room_form.html'

    def get_success_url(self):
        return reverse_lazy('room', kwargs={'pk': self.kwargs.get('pk')})


class DeleteRoomView(LoginRequiredMixin, generic.DeleteView):
    model = models.Room
    template_name = 'delete.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('home')


class DeleteMessageView(LoginRequiredMixin, generic.DeleteView):
    model = models.Message
    template_name = 'delete.html'
    context_object_name = 'obj'
    pk_url_kwarg = 'pk'

    def get_success_url(self):
        return reverse_lazy('room', kwargs={'pk': self.kwargs.get('pk_room')})
