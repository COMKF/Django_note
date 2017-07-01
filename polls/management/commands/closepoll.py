from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll
from django.utils import translation


# 自定义Command命令，格式为 python manage.py closepoll 参数
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # 该方法定义参数，若没有该方法，则无法添加参数。
    # 自定义命令应该覆盖此方法以添加命令接受的位置和可选参数。
    def add_arguments(self, parser):
        # 定义位置参数
        parser.add_argument('poll_id', nargs='+', type=int)

        # 定义可选参数
        # 例如，python manage.py closepoll 1 --delete，可以删除pk=1的记录
        parser.add_argument(
            # 实际上，以下代码只定义了一个命令参数（--delete），其他的都是该参数的一些附加属性。
            '--delete',  # 定义可选参数的形式，写成--delete，则命令后面写--delete。
            action='store_true',
            dest='delete',
            default=False,
            help='Delete poll instead of closing it',   # 帮助信息下，该参数的提示信息（--help可打开帮助信息）
        )

    # 该方法是命令的实际逻辑。子类必须实现此方法。
    def handle(self, *args, **options):
        for poll_id in options['poll_id']:
            try:
                poll = Poll.objects.get(pk=poll_id)
            except Poll.DoesNotExist:
                # 返回一个异常，它可以在控制台上打印
                raise CommandError('Poll "%s" does not exist' % poll_id)

            # 若可选参数中有 delete ，则执行删除
            if options['delete']:
                poll.delete()

            poll.opened = False
            poll.save()

            # 在控制台上打印
            self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))
'''
类BaseCommand--所有管理命令最终的基类。
作用：访问解析命令行参数的所有机制，并制定响应中调用的代码。
实现：对BaseCommand类进行子类化需要实现handle()方法。


'''