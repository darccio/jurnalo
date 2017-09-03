from graphene_django.views import GraphQLView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views
from django.conf.urls import url
from django.contrib import admin


class PrivateGraphQLView(LoginRequiredMixin, GraphQLView):
    pass


urlpatterns = [
    url(r'^accounts/login/$', views.login, {'template_name': 'admin/login.html'}),
    url(r'^accounts/logout/$', views.logout),
    url(r'^admin/', admin.site.urls),
    #url(r'^graphql$', PrivateGraphQLView.as_view(graphiql=True)),
]

