class StreamStatsError(Exception):
    '''Базовый тип ошибок в модуле streamstats'''

class UnsupportedFormatError(StreamStatsError):
    '''Ошибка при выборе неподдержываемого формата'''

class InvalidEventError(StreamStatsError):
    '''Ошибка при чтении неверного события'''

class InvalidTimestampError(StreamStatsError):
    '''Ошибка при чтении неверной временной метке'''

class CLIConfigError(StreamStatsError):
    '''Ошибка конфигурации CLI'''

class ReportError(StreamStatsError):
    '''Ошибка при составлении отчета'''
