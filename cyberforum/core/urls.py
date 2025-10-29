import core.views

from django.urls import path


app_name = "core"

urlpatterns = [
    path("", core.views.home_view, name="home"),
    path("contacts/", core.views.contacts_view, name="contacts"),
    path("textbooks/", core.views.textbooks_view, name="textbooks"),
    path(
        "moderator/textbooks/",
        core.views.textbook_moderator_list,
        name="textbook_moderator_list",
    ),
    path("moderator/textbooks/create/", core.views.textbook_create, name="textbook_create"),
    path(
        "moderator/textbooks/delete/<int:textbook_id>/",
        core.views.textbook_delete,
        name="textbook_delete",
    ),
    path("faq/", core.views.faq_view, name="faq"),
    path("chat-ask/", core.views.chat_ask, name="chat_ask"),
    path("register/", core.views.register_view, name="register"),
    path("login/", core.views.login_view, name="login"),
    path("logout/", core.views.logout_view, name="logout"),
    path("profile/", core.views.profile_view, name="profile"),
    path(
        "confirm-email/<uidb64>/<token>/",
        core.views.confirm_email_view,
        name="confirm_email",
    ),
    path("moderator/reports/", core.views.event_report_list, name="event_report_list"),
    path(
        "moderator/reports/create/",
        core.views.event_report_create,
        name="event_report_create",
    ),
    path('moderator/reports/export/', core.views.export_reports_to_excel, name='export_reports_excel'),
]
