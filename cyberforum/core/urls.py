from django.urls import path

from core import views


app_name = "core"

urlpatterns = [
    path("", views.home_view, name="home"),
    path("contacts/", views.contacts_view, name="contacts"),
    path("textbooks/", views.textbooks_view, name="textbooks"),
    path(
        "moderator/textbooks/",
        views.textbook_moderator_list,
        name="textbook_moderator_list",
    ),
    path("moderator/textbooks/create/", views.textbook_create, name="textbook_create"),
    path(
        "moderator/textbooks/delete/<int:textbook_id>/",
        views.textbook_delete,
        name="textbook_delete",
    ),
    path("faq/", views.faq_view, name="faq"),
    path("chat-ask/", views.chat_ask, name="chat_ask"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path(
        "confirm-email/<uidb64>/<token>/",
        views.confirm_email_view,
        name="confirm_email",
    ),
    path("moderator/reports/", views.event_report_list, name="event_report_list"),
    path(
        "moderator/reports/create/",
        views.event_report_create,
        name="event_report_create",
    ),
    path('moderator/reports/export/', views.export_reports_to_excel, name='export_reports_excel'),
]
