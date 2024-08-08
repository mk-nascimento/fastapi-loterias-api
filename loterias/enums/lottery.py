from enum import Enum


class Lottery(str, Enum):
    QUINA = 'quina'
    FEDERAL = 'federal'
    MEGA_SENA = 'megasena'
    DUPLA_SENA = 'duplasena'
    LOTOFACIL = 'lotofacil'
    LOTOMANIA = 'lotomania'
    SUPER_SETE = 'supersete'
    TIMEMANIA = 'timemania'
    DIA_DE_SORTE = 'diadesorte'
    MAIS_MILIONARIA = 'maismilionaria'
