import os
from livereload import Server
from django.core.management.commands.runserver import Command as RunServer

class Command(RunServer):
    def handle(self, *args, **options):
        server = Server()

        # Watch all files in the project directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Recursively watch all files and subdirectories
        server.watch(project_root)

        # Serve on the default livereload port (35729) and specify the project root
        server.serve(port=35729, root=project_root)

        # Start the Django development server
        super().handle(*args, **options)
