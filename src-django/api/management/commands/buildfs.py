from django.core.management.base import BaseCommand
from api.utils.routines import buildProjectsDir 

class Command(BaseCommand):
    help = "Builds the virtual filesystem from GitHub and blog data"

    def handle(self, *args, **kwargs):
        buildProjectsDir()
        self.stdout.write(self.style.SUCCESS("Filesystem built successfully."))
