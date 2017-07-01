# urls.py 就是一个映射文件，它包含一个或多个映射。
#
# urlpatterns = [
#     url(r'^$', views.index, name='index'),
# ]
from django.conf.urls import url
from django.contrib import admin

from . import views

# 现在这个项目只有一个polls应用程序，而在真正的项目中，可能会有多个应用程序，那么Django如何区分他们的URL名称（即name属性值）。
# 最好的做法是，为URLconf添加命名空间。在polls/urls.py文件中，添加一个app_name的属性，进行赋值，设置应用程序的命名空间，用来区分不同的应用程序。
# 需哟注意的是，如果有的模版使用了name作链接，那么这些链接就需要更改，在name前加上app_name:。

app_name = 'polls'
'''
urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # url()的三个参数，第一个是客户端请求，相当于Servlet，第二个是视图的函数（一般包含在py文件中），views就是py文件，index是函数。
    # 第三个是命名关键字参数，name。可从Django其他地方明确地引用它，特别是在模板中。

    # ex: /polls/5/
    url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # (?P<question_id>[0-9]+)，解析这句代码：
    # ?P<question_id>定义一个参数名为question_id的参数。
    # [0-9]+是用于匹配数字序列（即数字）的正则表达式。
    # 因此，这句代码获取了一个 question_id = [0-9]+ 的参数，

    # ex: /polls/5/results/
    url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),

    # ex: /polls/5/vote/
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
]
'''

# 在开发时，我们注意到有一部分页面是相似的，有些代码也是相似的（或者说相同的），这时我们需要用到一个新的技术：通用视图。
'''
只需要采取几个步骤进行转换
1.转换URLconf。（修改polls/urls.py文件）
2.删除一些旧的，不需要的视图。（修改polls/views.py文件）
3.替换成基于Django通用视图的新视图。
'''
# 这里修改了 index ， detail ， result 三个URL ，vote 作为参照不修改。
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # url(r'^$', admin.site.urls),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'templates/polls/add/$', views.addView.as_view(), name='add'),
    url(r'templates/polls/question/$', views.questionView.as_view(), name='question'),
]