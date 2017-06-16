import datetime
from django.utils import timezone
from django.test import TestCase
from .models import Question
from django.urls import reverse

# 学会使用assert的方法--断言
# 下面是方法测试
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        # 测试用例，是一个  发布时间 = 当前时间 + 30 天的Question实例。
        future_question = Question(pub_date=time)

        self.assertIs(future_question.was_published_recently(), False)  # 判断bool型变量是否相同
        '''
        测试过程：
        （如果在命令行运行python manage.py test polls的话：
        1.寻找polls程序中的tests.py文件。
        2.找到TestCase类的子类。
        ）
        3.为测试创建一个特殊的数据库。
        4.找到以test开头的方法进行测试。
        5.输入测试结果，并调用assertIs方法进行判断。返回False说明测试不通过，需要修改被测试的方法。
        6.销毁为测试生成的数据库。
        '''

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


# 下面是客户端测试
# 需要注意的是：数据库为每个测试方法重置，所以在测试的时候，需要自己添加数据，否则没有任何数据。
def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))  # 客户端获取 polls:index 的返回值
        self.assertEqual(response.status_code, 200)  # 判断两个值是否相等
        self.assertContains(response, "No polls are available.")  # 判断 前者是否包含后者
        self.assertQuerysetEqual(response.context['latest_question_list'], [])  # 判断数组或集合（list或tuple）是否相等

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


# 时间测试（也属于方法测试）
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


# 最好遵循以下规则：1.TestClass每个模型或视图分开 2.您要测试的每组条件，都需要有一个单独的测试方法 3.测试方法名称的名称最好能描述它的功能
