from django.urls import path
from .views import (
    ICaseListView,
    ICaseCreateView,
    ICaseDetailView,
    TPlanCreateView,
    ICaseUpdateView,
    ICaseDeleteView,
    get_tables,
    dj_code_generate,
)

app_name = "icases"
urlpatterns = [
    path("", ICaseListView.as_view(), name="icase-list"),
    path("icase/create/", ICaseCreateView.as_view(), name="icase-create"),
    path("icase/<int:pk>/", ICaseDetailView.as_view(), name="icase-detail"),
    path("icase/<int:pk>/update", ICaseUpdateView.as_view(), name="icase-edit"),
    path("icase/<int:pk>/delete", ICaseDeleteView.as_view(), name="icase-delete"),
    path(
        "icase/tplan/create/",
        TPlanCreateView.as_view(),
        name="tplan-create",
    ),
    path("table/<str:app_name>", get_tables, name="get-tables"),
    path(
        "table/<str:app_name>/<str:model_name>/generate",
        dj_code_generate,
        name="dj-code-generate",
    ),
    # path("icase/<int:pk>/update/", ICaseUpdateView.as_view(), name="icase_update"),
    # path("icase/<int:pk>/delete/", ICaseDeleteView.as_view(), name="icase_delete"),
]
