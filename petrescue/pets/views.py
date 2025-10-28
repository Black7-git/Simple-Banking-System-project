from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.db.models import Q

from .models import PetReport, ReportType, PetSpecies
from .forms import PetReportForm, PetInquiryForm


def home(request: HttpRequest) -> HttpResponse:
    recent_reports = PetReport.objects.all()[:10]
    return render(request, "pets/home.html", {"recent_reports": recent_reports})


def create_report(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = PetReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            messages.success(
                request,
                f"Report submitted. Your reference code is {report.reference_code}.",
            )
            return redirect("pets:report_detail", reference_code=report.reference_code)
    else:
        form = PetReportForm()
    return render(request, "pets/report_form.html", {"form": form})


def report_detail(request: HttpRequest, reference_code: str) -> HttpResponse:
    report = get_object_or_404(PetReport, reference_code=reference_code)
    return render(request, "pets/report_detail.html", {"report": report})


def search_reports(request: HttpRequest) -> HttpResponse:
    query = request.GET.get("q", "").strip()
    report_type = request.GET.get("type", "").strip()
    species = request.GET.get("species", "").strip()
    reports = PetReport.objects.all()
    if query:
        reports = reports.filter(
            Q(reference_code__iexact=query)
            | Q(location__icontains=query)
            | Q(description__icontains=query)
            | Q(color__icontains=query)
            | Q(breed__icontains=query)
        )
    if report_type in {choice for choice, _ in ReportType.choices}:
        reports = reports.filter(report_type=report_type)
    if species in {choice for choice, _ in PetSpecies.choices}:
        reports = reports.filter(species=species)

    inquiry_form = PetInquiryForm()
    return render(
        request,
        "pets/search.html",
        {"reports": reports[:50], "query": query, "inquiry_form": inquiry_form},
    )

# Create your views here.
