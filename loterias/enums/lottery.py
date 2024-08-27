from enum import Enum


class Lottery(str, Enum):
    DIA_DE_SORTE = 'diadesorte'
    DUPLA_SENA = 'duplasena'
    LOTERIA_FEDERAL = 'federal'
    LOTOFACIL = 'lotofacil'
    LOTOMANIA = 'lotomania'
    MAIS_MILIONARIA = 'maismilionaria'
    MEGA_SENA = 'megasena'
    QUINA = 'quina'
    SUPER_SETE = 'supersete'
    TIMEMANIA = 'timemania'
