from loguru import logger

logger.remove() # disable to print log data in linux teminal or console
logger.add("logs/greengook_{time:DD_MM_YYYY}.log", format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")
loglogger = logger