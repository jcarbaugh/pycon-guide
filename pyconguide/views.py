from django.http import HttpResponse
from django.utils import timezone
from django.views.generic import View, DetailView, ListView, TemplateView
from .models import Presentation, Interest, Calendar
from .calendar import generate_ical


class IndexView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            view = PresentationListView.as_view()
        else:
            view = LoginView.as_view()
        return view(request, *args, **kwargs)


class LoginView(TemplateView):
    template_name = 'login.html'


class PresentationListView(ListView):
    model = Presentation
    template_name = 'presentation_list.html'

    # def get_queryset(self):
    #     qs = super(ListView, self).get_queryset()
    #     qs = qs.filter(end_time__gte=timezone.now())
    #     return qs

    def get_context_data(self):
        context = super(PresentationListView, self).get_context_data()
        if self.request.user.is_authenticated():
            qs = Interest.objects.filter(
                user=self.request.user
            ).values_list('presentation__presentation_id', flat=True)
            context['interested_in'] = list(qs)
        else:
            context['interested_in'] = []
        return context


class CalendarView(DetailView):

    model = Calendar

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        presentations = Presentation.objects.filter(
            interests__user_id=obj.user)
        content = generate_ical(presentations)
        return HttpResponse(content, content_type='text/calendar')
