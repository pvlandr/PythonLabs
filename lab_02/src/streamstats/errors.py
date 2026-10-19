class StreamStatsError(Exception):
    '''Базовый тип ошибок в модуле streamstats'''
    pass

class UnsupportedFormatError(StreamStatsError):
    '''Ошибка при выборе неподдержываемого формата'''
    pass

class InvalidEventError(StreamStatsError):
    '''Ошибка при чтении неверного события'''
    pass

class InvalidTimestampError(StreamStatsError):
    '''Ошибка при чтении неверной временной метке'''
    pass

class CLIConfigError(StreamStatsError):
    '''Ошибка конфигурации CLI'''
    pass

class ReportError(StreamStatsError):
    '''Ошибка при составлении отчета'''
    pass