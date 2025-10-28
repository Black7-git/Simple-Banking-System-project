from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .models import PetReport, Claim


class ReportListView(ListView):
    model = PetReport
    template_name = "pets/report_list.html"
    context_object_name = "reports"


class ReportDetailView(DetailView):
    model = PetReport
    template_name = "pets/report_detail.html"
    context_object_name = "report"


class ReportCreateView(CreateView):
    model = PetReport
    fields = [
        "pet_name",
        "species",
        "breed",
        "color",
        "description",
        "location_found",
        "date_found",
        "photo",
        "contact_name",
        "contact_email",
        "contact_phone",
    ]
    template_name = "pets/report_form.html"
    success_url = reverse_lazy("pets:report_list")

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.reporter = self.request.user
        return super().form_valid(form)


class ClaimCreateView(CreateView):
    model = Claim
    fields = [
        "claimer_name",
        "claimer_email",
        "claimer_phone",
        "message",
        "proof_photo",
    ]
    template_name = "pets/claim_form.html"

    def form_valid(self, form):
        form.instance.pet_id = self.kwargs["pk"]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("pets:report_detail", kwargs={"pk": self.kwargs["pk"]})


class SearchView(ListView):
    model = PetReport
    template_name = "pets/search.html"
    context_object_name = "results"

    def get_queryset(self):
        qs = super().get_queryset().filter(status="found")
        q = self.request.GET.get("q", "").strip()
        species = self.request.GET.get("species", "").strip()
        color = self.request.GET.get("color", "").strip()
        location = self.request.GET.get("location", "").strip()

        if q:
            qs = qs.filter(
                Q(pet_name__icontains=q)
                | Q(description__icontains=q)
                | Q(breed__icontains=q)
            )
        if species:
            qs = qs.filter(species=species)
        if color:
            qs = qs.filter(color__icontains=color)
        if location:
            qs = qs.filter(location_found__icontains=location)
        return qs

