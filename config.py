# -*- coding: utf-8 -*-
class BaseConfig:
    """Base configuration."""
    DEBUG = False


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
