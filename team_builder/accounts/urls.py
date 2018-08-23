from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^account/$', views.account_redirect, name='redirect'),
    url(r"logout/$", views.LogoutView.as_view(), name="logout"),
    url(r"signup/$", views.SignUpView.as_view(), name="signup"),
    url(r"profile/(?P<pk>\d+)/$", views.ProfileDetailView.as_view(), name="profile"),
    url(r'edit/(?P<pk>\d+)/$', views.ProfileEditView.as_view(),
        name='edit_profile'),
]
