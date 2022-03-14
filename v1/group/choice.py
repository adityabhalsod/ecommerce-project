from django.contrib.gis.db import models


class Level(models.TextChoices):
    ONE = "level 1", "Level 1"
    TWO = "level 2", "Level 2"
    THREE = "level 3", "Level 3"


class Alignment(models.TextChoices):
    HORIZONTAL = "horizontal", "Horizontal"
    VERTICAL = "vertical", "Vertical"
