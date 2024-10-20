from django.urls import path

from .views import user_detail_view
from .views import user_redirect_view
from .views import *
app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:pk>/", view=user_detail_view, name="detail"),
    path('upload_clients/', upload_clients_view, name='upload_clients'),
    path('export_clients/<int:company_id>/', export_clients_excel, name='export_clients_excel'),
    path('login/', LoginView.as_view(), name='login'),
    path("logout/", logout_view, name="logout"),
    path("change_password/", change_password_view, name="change_password"),
    path('company_analytics/<int:company_id>/', CompanyAnalyticsAPIView.as_view(), name='company-analytics'),
    path("all_companies/", view=AllCompaniesAPi.as_view(), name="all-companies-api"),
    path("all_clients/", view=AllClientsAPi.as_view(), name="all-clients-api"),
    path('client_by_national_id/<str:national_id>/', ClientByNationalIdAPIView.as_view(), name='client-by-national-id'),

    path("add_company/", view=AddCompanyView.as_view(), name="add-company-api"),
    path('upload_clients/<int:company_id>/', UploadClientsAPIView.as_view(), name='upload_clients'),

    # path('export-clients/<int:company_id>/', export_clients_excel, name='export_clients_excel'),
]
