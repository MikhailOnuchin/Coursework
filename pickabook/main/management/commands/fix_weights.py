from django.core.management.base import BaseCommand
from ...complementary.recommendation_scripts import check_preferences


class Command(BaseCommand):
    help = 'Fixes user tag weights'

    def handle(self, *args, **options):
        check_preferences.check_all()
