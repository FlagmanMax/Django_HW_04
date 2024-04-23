from django.core.management.base import BaseCommand
from seminar3.models import Author, Post, Comment

LOREM = "Lorem ipsum dolor sit amet, consectetur adipisicingelit. " \
"Accusamus accusantium aut beatae consequaturconsequuntur cumque, delectus et illo iste maxime " \
"nihil non nostrum odio officia, perferendis placeatquasi quibusdam quisquam quod sunt " \
"tempore temporibus ut voluptatum? A aliquam culpaducimus, eaque eum illo mollitia nemo."


class Command(BaseCommand):
    help = "Generate fake comments."

    def add_arguments(self, parser):
        parser.add_argument('author_id', type=int, help='Author ID')

    def handle(self, *args, **kwargs):
        author_id = kwargs.get('author_id')
        author = Author.objects.filter(pk=author_id).first()
        posts = Post.objects.filter(author=author_id).all()
        for post in posts:
            comment = Comment(author=author,
                              post=post,
                              comment=LOREM)
            comment.save()
