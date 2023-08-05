# Copyright 2015 VPAC
#
# This file is part of Karaage.
#
# Karaage is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Karaage is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Karaage  If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import url, include
from django.conf import settings

from karaage.plugins.kgusage import views

urlpatterns = [
    url(r'^$', views.usage_index, name='kg_usage_list'),

    url(r'^unknown/$', views.unknown_usage, name='kg_usage_unknown'),

    url(r'^search/$', views.search, name='kg_usage_search'),
    url(r'^jobs/$', views.job_list, name='kg_usage_job_list'),
    url(r'^jobs/(?P<jobid>[-.\w\[\]]+)/$',
        views.job_detail, name='kg_usage_job_detail'),

    url(r'^(?P<machine_category_id>\d+)/$', views.index, name='kg_usage_mc'),

    url(r'^(?P<machine_category_id>\d+)/core_report/$',
        views.core_report, name='kg_usage_core_report'),
    url(r'^(?P<machine_category_id>\d+)/mem_report/$',
        views.mem_report, name='kg_usage_mem_report'),
    url(r'^(?P<machine_category_id>\d+)/trends/$',
        views.institute_trends, name='kg_usage_institute_trends'),

    url(r'^(?P<machine_category_id>\d+)/institute/(?P<institute_id>\d+)/$',
        views.institute_usage, name='kg_usage_institute'),
    url(r'^(?P<machine_category_id>\d+)/institute/'
        r'(?P<institute_id>\d+)/users/$',
        views.institute_users, name='kg_usage_users'),
    url(r'^(?P<machine_category_id>\d+)/projects/(?P<project_id>%s)/$'
        % settings.PROJECT_VALIDATION_RE,
        views.project_usage, name='kg_usage_project'),

    url(r'^(?P<machine_category_id>\d+)/top_users/$',
        views.top_users, name='kg_usage_top_users'),

    url(r'^software/(?P<software_id>\d+)/stats/$',
        views.software_stats, name='kg_software_stats'),
    url(r'^software_version/(?P<version_id>\d+)/stats/$',
        views.version_stats, name='kg_software_version_stats'),
]

urlpatterns = [
    url(r'^usage/', include(urlpatterns)),
]
