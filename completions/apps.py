"""Configuration module for the FavoriteCart app."""

from django.apps import AppConfig


class CompletionsConfig(AppConfig):
    """Main config data structure for the completions app."""

    name = 'completions'

    def ready(self):
        """Initializations to be performed with the app is ready."""
        try:
            from . import signals
        except ImportError:
            pass
