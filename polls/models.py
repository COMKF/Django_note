# 创建模型，相当于Java中的类。有自己的名称和属性。同时也是数据库布局。
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

'''
每个模型都由一个类来表示django.db.models.Model。每个模型都有一些类变量，每个变量都表示模型中的数据库字段。

每个字段由Field 类的实例表示- 例如，CharField用于字符字段和 DateTimeField数据时间。这告诉Django每个字段拥有什么类型的数据。
每个Field实例的名称（例如 question_text或pub_date）是字段的名称。将在Python代码中使用此值，数据库将使用它作为列名。
您可以使用可选的第一个位置参数来 Field指定人类可读的名称。这用于Django的几个内省部分，它可以作为文档。
如果未提供此字段，Django将使用机器可读的名称。
在这个例子中，我们只定义了一个可读的名字Question.pub_date。对于此模型中的所有其他字段，该字段的机器可读名称将足以作为其可读的名称。

一些Field类有必要的参数。 CharField例如，要求你给它一个 max_length。这不仅在数据库模式中使用，而且可用于验证。
A Field也可以有各种可选参数; 在这种情况下，我们将default值 设置votes为0。
最后，注意一个关系的定义，使用 ForeignKey。这告诉Django每个Choice都与一个相关Question。Django支持所有常见的数据库关系：多对一，多对多和一一对应。
'''
@python_2_unicode_compatible  # only if you need to support Python 2
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')   # 日期类型数据，并定义'date published'作为人类可读的名称。
    def __str__(self):
    # 为模型添加__str__()方法非常重要，这不仅在处理交互式提示时方便您使用，还能让管理员通过直观但表示更好但管理Django。
    # 当在shell窗口下调用Question.objects.all()时，会打印所有的Question，其实调用的就是__str__方法，生成一个Set并返回。
        return self.question_text

    '''
    def was_published_recently(self): #一个自定义的方法，用于测试
        # 这个方法的目的是，判断一个Question实例是不是最近发布的。方法： 发布时间 >= 当前时间 -1
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    '''
    # 我们发现这个方法有缺陷，现在对它进行改进，同时，该方法可以定义虚拟字段
    def was_published_recently(self):
        now = timezone.now()
        # 更改后的方法：昨天<=当前时间<=明天
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # 对was_published_recently方法显示的内容进行定义：boolean属性指定该字段显示为图表，short_description列标题显示内容，admin_order_field排序字段
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


@python_2_unicode_compatible  # only if you need to support Python 2
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    #设置外健
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

'''
这些模型代码给了Django很多信息。有了它，Django能够：
    1.为此应用程序创建数据库模式（语句）。CREATE TABLE。
    2.创建用于访问Question和Choice对象的Python数据库访问API 。
但首先我们需要告诉我们的项目该polls应用是安装的。
另外，Django应用程序（如polls就是一个应用程序）是“可插拔”：您可以在多个项目中使用应用程序，您可以分发应用程序，因为它们不必与给定的Django安装绑定。

那么如何在项目中使用这个应用程序呢？
要将该应用程序包括在我们的项目中，我们需要在设置中添加对其配置类的引用INSTALLED_APPS。
polls的PollsConfig配置在polls/apps.py文件中，所以它的虚线路径'polls.apps.PollsConfig'。
编辑mysite/settings.py文件，并将该虚线路径添加到该INSTALLED_APPS设置。

然后，我们需要应用这些更改到数据库中。

总体来说，分三步：
改变你的模型（in models.py）。
运行以创建这些更改的迁移python manage.py makemigrations polls
运行以将这些更改应用于数据库。python manage.py migrate
'''
'''
接下来，我们尝试着使用Python shell，使用这个python manage.py shell命令。
我们使用这个，而不是简单地输入“python”，
因为manage.py 设置了DJANGO_SETTINGS_MODULE环境变量，这为Django提供了你的mysite/settings.py文件里的Python路径。

进入Shell编程。
然后，在命令行窗口下探索数据库API。
键入命令 from polls.models import Question,Choice ＃导入我们刚写的模型类。
键入命令 Question.objects.all() ＃查看所有的Question
    与这个命令相似的命令：
        Question.objects.filter(id=1)    # 查询 id = 1 的Question
        Question.objects.filter(question_text__startswith='What') # 查询以'What'开头的question_text的Question。
        Question.objects.get(pub_date__year=current_year) # 获取pub_date的year等于current_year（变量，需自己设置）的Question。
        Question.objects.get(id=1) # 获取 id = 1 的Question，它与外健获取Question.objects.get(pk=1)是相等的。

键入命令 from  django.utils  import  timezone
在默认设置文件中启用对时区的支持，所以Django需要一个tzinfo的datetime为pub_date。使用timezone.now（）。

键入命令 q = Question(question_text="What's new?", pub_date=timezone.now()) #生成一个Question实例
键入命令 q.save() #保存q到数据库中，必须显式调用save（）。
    可以直接查看q的属性，如q.question_text，也可以直接更改q.question_text = "为什么"，但更改后要记住保存：q.save() 。
    
如何创建Choice？？
首先，我们知道Choice的外健是Question的主键。
所以
1.先获取一个Question实例，q = Question.objects.get(id=1)。
2.通过q.choice_set.create(choice_text='Just hacking again', votes=0)进行创建。不需要调用save()方法。
当然，也可以写成 c = q.choice_set.create(choice_text='Just hacking again', votes=0)，把结果保存在变量c中。

键入命令 c = q.choice_set.filter(choice_text__startswith='Just hacking') #获取一个Choice实例。
键入命令 c.delete() #可以在数据库里删除这条记录。
'''

'''
退出Shell编程。
我们尝试着创建一个超级管理员。
键入命令 python manage.py createsuperuser，然后根据命令输入即可。
现在，为们可以登录管理员页面了。http://127.0.0.1:8000/admin/。

注意事项：

1.表单是从Question模型自动生成的。
2.不同的模型字段类型（DateTimeField， CharField）对应于适当的HTML输入小部件。每种类型的字段知道如何在Django管理员中显示自己。
3.每个都DateTimeField获得免费的JavaScript快捷方式。
日期获取“Today”快捷方式和日历弹出窗口，并且时间获取“Now”快捷方式和一个方便的弹出窗口，列出常用的时间。
'''