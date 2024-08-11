from logging import BASIC_FORMAT

from pytz import all_timezones, timezone

_SPLITTED_FMT = BASIC_FORMAT.split(':')
_SPLITTED_FMT.insert(1, '%(asctime)s')


LOGGING_FORMAT = f'{_SPLITTED_FMT[0]}:\t{" - ".join(_SPLITTED_FMT[1:3])}\n\t{_SPLITTED_FMT[-1]}'

BR_TZ = next(tz for tz in all_timezones if 'Sao_Paulo' in tz)
BRAZILIAN_TIMEZONE = timezone(BR_TZ)
SEC_IN_MINUTE, MIN_IN_HOUR, HOURS_IN_DAY = (60, 60, 24)
