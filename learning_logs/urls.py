from django.urls import path

from .views import (
    HomePageView,
    TopicListView,
    TopicDetailView,
    TopicCreateView,
    TopicDeleteView,
    EntryCreateView,
    EntryUpdateView,
    EntryDetailView,
    EntryDeleteView,
)

urlpatterns = [
    path("topics/", TopicListView.as_view(), name="topic_list"),
    path("topics/new/", TopicCreateView.as_view(), name="topic_new" ),
    path("topics/<int:pk>/", TopicDetailView.as_view(), name="topic_detail"),
    path("topics/<int:pk>/delete/", TopicDeleteView.as_view(), name="topic_delete"),
    path("entry/<int:pk>/new/", EntryCreateView.as_view(), name="entry_new"),
    path("entry/<int:pk>/edit/", EntryUpdateView.as_view(), name="entry_edit"),
    path("entry/<int:pk>/detail/", EntryDetailView.as_view(), name="entry_detail"),
    path("entry/<int:pk>/delete/", EntryDeleteView.as_view(), name="entry_delete"),
    path("", HomePageView.as_view(), name="home"),
]
