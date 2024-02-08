from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import ICase, ICaseDetail, ICaseImage, TPlan, TPlanDetail
from .forms import ICaseForm, TPlanForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connection
from config.utils import get_table_app, get_dj_code_generate
from django.apps import apps


def get_tables(request, app_name):

    app_configs = apps.get_app_configs()
    app_names = [
        app_config.name
        for app_config in app_configs
        if "django" not in app_config.name
        if "allauth" not in app_config.name
        if "crispy" not in app_config.name
        if "server" not in app_config.name
    ]

    if app_name == "all":

        with connection.cursor() as cursor:
            all_table_names = connection.introspection.table_names()
            app_table_names = [name for name in all_table_names]
            table_columns = {
                table: connection.introspection.get_table_description(cursor, table)
                for table in app_table_names
            }

        return render(
            request,
            "icases/table.html",
            {
                "table_columns": table_columns,
                "app_name": app_name,
                "app_names": app_names,
            },
        )
    else:

        with connection.cursor() as cursor:
            all_table_names = connection.introspection.table_names()
            app_table_names = [
                name for name in all_table_names if name.startswith(app_name + "_")
            ]
            table_columns = {
                table: connection.introspection.get_table_description(cursor, table)
                for table in app_table_names
            }
            # print("table_columns: ", table_columns)
        return render(
            request,
            "icases/table.html",
            {
                "table_columns": table_columns,
                "app_name": app_name,
                "app_names": app_names,
            },
        )


def dj_code_generate(request, app_name, model_name):

    app_configs = apps.get_app_configs()
    app_names = [
        app_config.name
        for app_config in app_configs
        if "django" not in app_config.name
        if "allauth" not in app_config.name
        if "crispy" not in app_config.name
        if "debug" not in app_config.name
        if "server" not in app_config.name
    ]
    code_gen = get_dj_code_generate(app_name, model_name)
    table_columns = get_table_app(request, app_name)

    return render(
        request,
        "icases/dj_code_generate.html",
        {
            "code_gen": code_gen,
            "table_columns": table_columns,
            "app_name": app_name,
            "model_name": model_name,
            "app_names": app_names,
        },
    )


class ICaseListView(LoginRequiredMixin, ListView):

    model = ICase
    template_name = "icases/icase_list.html"
    context_object_name = "icases"
    paginate_by = 10

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ICase.objects.all()
        else:
            return ICase.objects.filter(user=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["table_columns"] = get_table_app(self.request, "icases")
        context["app_name"] = "icases"
        context["app_name_length"] = len("icases")
        # Add Status_choices to the context
        context["status_choices"] = ICase.STATUS_CHOICES

        return context


class ICaseDetailView(LoginRequiredMixin, DetailView):
    model = ICase
    template_name = "icases/icase_detail.html"
    context_object_name = "icase"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["icase_comments"] = ICaseComment.objects.filter(icase=self.object)
        return context


class ICaseUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, pk):
        icase = ICase.objects.get(pk=pk)
        form = ICaseForm(instance=icase)
        return render(request, "icases/icase_edit.html", {"form": form})

    def post(self, request, pk):
        icase = ICase.objects.get(pk=pk)
        form = ICaseForm(request.POST, request.FILES, instance=icase)

        if form.is_valid():
            form.save()
            return redirect("icases:icase-detail", pk=icase.pk)
        return render(request, "icases/icase_edit.html", {"form": form})

    def get_success_url(self):
        return reverse("icases:icase-detail", kwargs={"pk": self.object.pk})


class ICaseDeleteView(LoginRequiredMixin, DeleteView):
    model = ICase
    template_name = "icases/icase_delete.html"
    context_object_name = "icase"

    def get_success_url(self):
        return reverse("icases:icase-list")


class ICaseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        staffs = request.user.is_staff
        context = {
            "form": ICaseForm(),
            "staffs": staffs,
        }

        return render(request, "icases/icase_create.html", context)

    def post(self, request):
        form = ICaseForm(request.POST, request.FILES)

        if form.is_valid():
            icase = form.save(commit=False)
            icase.user = request.user
            # print("icase.report: ", icase.report)
            icase.save()
            return redirect("icases:icase-detail", pk=icase.pk)
        return render(request, "icases/icase_create.html", {"form": form})


class TPlanCreateView(CreateView):
    model = TPlan
    template_name = "icases/tplan_create.html"
    fields = [
        "category",
        "target_cost",
        "name",
        "description",
        "report",
        "status",
        "tags",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "Draft"
        form.save()
        return super().form_valid(form)
