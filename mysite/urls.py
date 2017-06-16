"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
'''
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
'''
from django.conf.urls import include, url
from django.contrib import admin

'''
当有人从您的网站请求一个页面 - 例如“/ polls / 34 /”时，
1.Django将加载mysite.urls模块，因为ROOT_URLCONF设置指向它。
2.它找到mysite.urls中的变量urlpatterns，并按顺序遍历正则表达式。
3.找到匹配后'^polls/'，它将剥离匹配的文本（"polls/"），并将剩余的文本发送"34/"到“polls.urls”URLconf进行进一步处理。
4.它找到polls.urls中的变量urlpatterns，再匹配r'^(?P<question_id>[0-9]+)/$'，找到参数views.detail进行进一步处理。
5.找到views.py文件，从中找到detail函数，进行视图渲染并返回。
'''
urlpatterns = [

    url(r'^polls/', include('polls.urls')), # url()的两个参数，第一个是客户端请求，相当于Servlet，第二个是include函数，它的参数是映射的文件。
    url(r'^admin/', admin.site.urls),   # url()的两个参数，第一个是客户端请求，相当于Servlet，第二个是视图的函数（一般包含在py文件中）
]
# 该include()函数允许引用其他URLconfs。include()使即插即用的URL变得容易。

# 何时使用 include(),当包含其他网址格式时，应始终使用。 admin.site.urls是唯一的例外。