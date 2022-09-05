from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.test import Client

from .models import Topic, Entry

class LearningLogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", password="secret"
        )

        cls.topic = Topic.objects.create(
            title="Any topic",
            author=cls.user,
        )

        cls.entry = Entry.objects.create(
            topic=cls.topic,
            text="any text as an example",
        )
    
    def test_topic_model(self):
        self.assertEqual(self.topic.title, "Any topic")
        self.assertEqual(self.topic.author.username, "testuser")
        self.assertEqual(str(self.topic), "Any topic")

    def test_entry_model(self):
        self.assertEqual(self.entry.topic.title, "Any topic")
        self.assertEqual(self.entry.text, "any text as an example")
        self.assertEqual(self.entry.topic.author.username, "testuser")
        self.assertEqual(str(self.entry), "any text as an example")
        self.assertEqual(self.entry.get_absolute_url(), "/entry/1/detail/")

    def test_url_exists_at_correct_location_home_templateview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    