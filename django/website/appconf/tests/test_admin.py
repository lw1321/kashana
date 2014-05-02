import pytest
import mock
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import admin
from contacts.models import User
from ..admin import SettingsAdmin
from ..models import Settings


def test_add_view_redirects_to_index():
    index_url = reverse("admin:index")
    view = SettingsAdmin(Settings, None)
    response = view.add_view(None)

    assert response.url == index_url


def test_delete_view_redirects_to_index():
    index_url = reverse("admin:index")
    view = SettingsAdmin(Settings, None)
    response = view.delete_view(None, None)

    assert response.url == index_url


@pytest.mark.django_db
def test_changelist_view_redirects_to_change_url():
    s = Settings.objects.create()
    change_url = reverse("admin:appconf_settings_change", args=[s.id])
    view = SettingsAdmin(Settings, None)
    response = view.changelist_view(None)

    assert response.url == change_url


@pytest.mark.django_db
def test_change_view_does_not_redirect_on_get(rf):
    s = Settings.objects.create()
    change_url = reverse("admin:appconf_settings_change", args=[s.id])
    request = rf.get(change_url)
    request.user = mock.Mock(is_staff=True, is_superuser=True)
    request.user.has_perm = mock.Mock(return_value=True)

    view = SettingsAdmin(Settings, admin.site)
    response = view.change_view(request, str(s.id))

    assert isinstance(response, HttpResponseRedirect) is False
