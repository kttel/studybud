from base import models


class RoomFormMixin:
    def form_valid(self, form):
        form.instance.host = self.request.user
        topic, created = models.Topic.objects.get_or_create(
            name=self.request.POST.get('topic'),
        )
        form.instance.topic = topic
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['topics'] = models.Topic.objects.all()
        return context
