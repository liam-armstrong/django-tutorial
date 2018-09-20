import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import *

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        # was_published_recently returns false for questions whose pub_dates are in the future
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
    
    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=3)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
    
def create_question(question_text, days):
    # create a question with given question_text and pub_date as number of days from today (positive for future, negative for past)
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionViewTests(TestCase):
    def test_no_questions(self):
        #If there are no questions, display an error message
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_past_question(self):
        #question with a pub_date in the past are published on the index page
        create_question(question_text = "Past Question", days= -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past Question>'])
        
    def test_future_question(self):
        #question with pub_date in the future isn't published on the index page
        create_question(question_text = "Future Question", days = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_future_and_past_questions(self):
        #only previously published question appears on index page when future question is also there
        create_question(question_text = "Future Question", days = 30)
        create_question(question_text = "Past Question", days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'], 
            ['<Question: Past Question>'])
    
    def test_two_past_questions(self):
        # both questions should appear on the index page
        create_question(question_text = "Past1", days = -30)
        create_question(question_text = "Past2", days = -35)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past2>', '<Question: Past1>'])
        
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        # makes sure a future question's detail page return 404
        future_question = create_question(question_text = "Future Question", days = 5)
        url = reverse('polls:detail', args(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_past_questions(self):
        # makes sure a past question's detail page returns a valid page
        past_question = create_question(question_text = "Past Question", days  = -5)
        url = reverse('polls;detail', args(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)