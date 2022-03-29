"""File to include any application configuration for the app."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """Defines configuration for blog app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
