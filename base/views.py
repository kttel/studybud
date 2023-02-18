from django.contrib.auth import views as login_views
from django.views import generic
from django.urls import reverse_lazy

from base import models, forms, utils


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
