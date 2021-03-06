from time import sleep
from django.conf import settings
from django.core.management.base import BaseCommand

# from config.managers import global_state
from photos.utils.organise import import_photos_in_place
from photos.utils.system import missing_system_dependencies


class Command(BaseCommand):
    help = 'Creates relevant database records for all photos that are in a folder.'

    def add_arguments(self, parser):
        parser.add_argument('--paths', nargs='+', default=[item['PATH'] for item in settings.PHOTO_OUTPUT_DIRS])

    def rescan_photos(self, paths):
        missing = missing_system_dependencies(['exiftool', ])
        if missing:
            print('Missing dependencies: {}'.format(missing))
            exit(1)

        for path in paths:
            import_photos_in_place(path)

    def handle(self, *args, **options):
        while True:
            # TODO: Add a lock in here because DB corruption occurs if rescan_photos is called while it's still already running
            # global_state.increment('photo_import_tasks_running')
            self.rescan_photos(options['paths'])
            # global_state.decrement('photo_import_tasks_running')

            sleep(60 * 60)  # Sleep for an hour
