from django.contrib import admin

from .models import Choice, Question


# admin.site.register(Question)   # 在理员索引页面上注册了Question,并能创建一个默认的表单

# 1.需要自定义管理表单的外观和工作原理。可以通过告诉Django注册对象时所需的选项来做到这一点。
# 创建模型管理类
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']  # 它的效果是使“出版日期”出现在“问题”字段之前。

# 然后将模型管理类作为第二个参数传递给admin.site.register()
# admin.site.register(Question, QuestionAdmin)


# 2.如果一个表单有几十个字段，可以将表单分成几个（字段的）集合。每个元组的第一个元素 fieldsets是字段集的标题
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]

# admin.site.register(Question, QuestionAdmin)

# 3.一个Question有多个 Choices，但管理页面不显示选择，怎么解决？
# 第一个方法是Choice 像Question一样向管理员注册。
# admin.site.register(Choice)
# 在该表单中，“问题”字段是包含数据库中每个问题的选择框。Django知道a ForeignKey应该在管理员中表示为一个<select>框。
# 问题在于，创建问题的时候，不能直接添加选择。或者在对问题进行编辑的时候，不能添加选择。该怎么解决呢？

# 第二个方法。Question与Choice绑定。
# class ChoiceInline(admin.StackedInline):  # 显示用于输入相关Choice对象的所有字段需要大量的屏幕空间。只需要将ChoiceInline声明更改为下即可。
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None, {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
#     ]
#     inlines = [ChoiceInline]
# admin.site.register(Question, QuestionAdmin)

# 4.自定义管理更改列表
# 默认情况下，Django显示str()每个对象。但有时如果我们可以显示个别的字段会更有帮助。
# 要做到这一点，可使用list_display选项，这是一个字段名称的元组，作为列显示在对象的更改列表页面。
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]  # 引用子对象
    list_display = ('question_text', 'pub_date', 'was_published_recently')  # 需要显示的列的列标题必须是字段或者方法（在Django里，两者没有区别）
    list_filter = ['pub_date']  # 添加过滤器的侧边栏，可以通过pub_date字段过滤更改列表。
    search_fields = ['question_text'] # 在表的顶部添加一个搜索栏
    # 显示的过滤器类型取决于您要过滤的字段类型。
    # 因为pub_date是DateTimeField，Django知道提供适当的过滤器选项：“任何日期”，“今天”，“过去7天”，“本月”，“今年”。


admin.site.register(Question, QuestionAdmin)
