from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.http import Http404
from django.template import loader
from django.urls import reverse
from .models import Choice, Question
from django.views import generic
from django.utils import timezone


# 这是一个视图，它需要一个映射。
# def index(request):
#   return HttpResponse("Hello, world. You're at the polls index.")

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)

# def index(request):
#    latest_question_list = Question.objects.order_by('-pub_date')[:5]
#    template = loader.get_template('polls/index.html')  # 加载模版
#    context = {
#        'latest_question_list': latest_question_list,
#    }
#    return HttpResponse(template.render(context, request))  # 用template.render方法渲染


# 除了用template.render方法渲染，Django还提供了一个快捷的渲染方法。当用了这种方法，就会发现，不需要导入loader和HttpResponse了。
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}  # context，dict类型的参数。
    return render(request, 'polls/index.html', context)
    # 用render()函数渲染，将请求对象作为其第一个参数，模板作为其第二个参数，第三个参数可选(事实上，第三个参数名不固定，但用context这个变量名是习惯)。
    # 它返回HttpResponse 给定上下文渲染的给定模板的对象。


# 接下来我们添加多个视图，当然，他们需要各自不同的映射。
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)

# def detail(request, question_id):
#     try:
#        question = Question.objects.get(pk=question_id) # pk也行id 也行，都是数据库的操作。
#     except Question.DoesNotExist:   # 如果发生请求的ID不存在的问题，则该视图引发异常.
#         raise Http404("Question does not exist")
#     return render(request, 'polls/detail.html', {'question': question})

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # 当然，也可以用更简单的get_object_or_404方法抛出异常。这个方法第一个参数是Django模型，然后是任意数量的关键字参数。
    return render(request, 'polls/detail.html', {'question': question})


# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        '''
        #request.POST是一个类似字典的对象（dict），可通过键名访问提交的数据。
        #request.POST['choice']，即 以选择的选项name作为键，获取对应的值。
        
        #请注意，Django还提供request.GET以相同的方式访问GET数据。但是我们request.POST在代码中明确使用，以确保仅通过POST调用更改数据。
        '''
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "你没有进行选择",
        })
    else:
        selected_choice.votes += 1  # 加1
        selected_choice.save()  # 然后保存
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
        # 重定向。reverse函数，第一个参数是 视图的name值，第二个参数指定了args参数，说明了要传递给下一个视图的参数。


# 删除老index，detail和results 视图，并使用Django的通用视图代替。（其实不删除也行，因为方法名称变了，调用不到它们了）
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'  # 指定传入模版的context对象的变量名，也就是为列表重新命名。

    # 因为这是父类是ListView，所以可以直接写 model = Question ，获取所有的Question实例，封装称列表。这样就不需要get_queryset(self)方法了。

    def get_queryset(self):  # 这个函数，将会获取查询到的列表集，并把结果返回给 context对象。
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    # get_queryset(self)方法与context_object_name变量，通常都是配合使用的。
    # 以上方法会在类视图调用as_view()后自动调用。


class DetailView(generic.DetailView):
    model = Question
    # 因为父类是DetailView，所以 model = Question ，获取的是具体对应的 model对象。
    # context_object_name不需要写，因为context_object_name默认为是model的小写变量，即question，模版上直接用question就行了。
    template_name = 'polls/detail.html'

    def get_queryset(self):#这个函数，将会获取查询到的列表集（实际上只有一个实例），并把结果返回给context对象的变量名（即model，Question对象）。
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())    # 对实例进行过滤，只获取过去的问题。



class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
'''
这里使用两个通用视图（其实有多种通用视图）： ListView和 DetailView。这两个视图分别提取了“显示对象列表”和“显示特定类型对象的详细信息页面”的概念。
1.每个通用视图都需要知道它将采取什么样的模式。这是使用model属性提供的。
2.DetailView通用视图预计从URL中捕获的主键值被调用 "pk"，所以我们已经改变question_id，以pk用于通用视图。

DetailView默认使用一个叫做<app name>/<model name>_detail.html的模版，但是我们可以使用template_name这个属性来指定Django需要加载的模版。
ListView同理。

我的个人理解：
在URL路径中，index没有出现pk，id等关键字，也就不需要model，用ListView就行了。且，ListView主要用于获取某个model列表。
而detail和results等的URL中，有pk这种关键字，必须指定model，否则关键字就无效了，用DetailView。且，DetailView主要用于获取某单个model对象。

'''


class addView(generic.ListView):
    template_name = 'polls/add.html'
    model = Question


class questionView(generic.ListView):
    template_name = 'polls/question.html'
    context_object_name = 'latest_question_list'  # 指定传入模版的context对象的变量名，也就是为列表重新命名。

    def get_queryset(self):  # 这个函数，将会获取查询到的列表集，并把结果返回给 context对象。
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


