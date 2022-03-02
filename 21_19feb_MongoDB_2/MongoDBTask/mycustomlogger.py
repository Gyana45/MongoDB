import logging
import inspect


class customlogger:
    @staticmethod
    def mylog(file_name='test.log', log_level=logging.DEBUG):
        # set the logger name from where it is called
        logger_name = inspect.stack()[1][3]
        print(logger_name)

        # create logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        # create handler
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(logging.INFO)

        # create formatter
        formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        file_handler.setFormatter(formatter)

        # adding handler to logger
        logger.addHandler(file_handler)

        return logger
