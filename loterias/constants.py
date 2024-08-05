from logging import BASIC_FORMAT

_SPLITTED_FMT = BASIC_FORMAT.split(':')
_SPLITTED_FMT.insert(1, '%(asctime)s')


LOGGING_FORMAT = f'{_SPLITTED_FMT[0]}:\t{" - ".join(_SPLITTED_FMT[1:3])}\n\t{_SPLITTED_FMT[-1]}'
