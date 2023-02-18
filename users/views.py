from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy

from users import utils, forms


class ProfileView(generic.DetailView):
    model = get_user_model()
    template_name = 'users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return utils.update_profile_context(context)


class UpdateProfileView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    form_class = forms.UserForm
    template_name = 'users/edit-user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('user-profile',
                            kwargs={'pk': self.request.user.pk})
