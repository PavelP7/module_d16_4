from django.core.management.base import BaseCommand
from news.models import Category, Post

class Command(BaseCommand):
    help = 'Удаление новостей указанной категории'
    missing_args_message = 'Укажите категорию'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', nargs='+', type=str)

    def handle(self, *args, **options):
        category = str(options['category'])[2:-2]
        if Category.objects.filter(topic=category).exists():
            self.stdout.readable()
            self.stdout.write('Confirm your action. Delete all posts? yes/no')
            answer = input()
            if answer == 'yes':
                Post.objects.filter(category__topic=category).delete()
                self.stdout.write(self.style.SUCCESS("Posts were deleted!"))
            else:
                self.stdout.write(self.style.ERROR("Access denied"))
        else:
            self.stdout.write(self.style.ERROR(f"Category {category} don't exist"))
