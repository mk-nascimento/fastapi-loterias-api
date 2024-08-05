from enum import Enum


class Environment(str, Enum):
    DEV = 'development'
    PROD = 'production'
