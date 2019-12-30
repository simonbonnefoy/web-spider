import logging


level = {
    0: logging.NOTSET,
    1: logging.INFO,
    2: logging.DEBUG,
    3: logging.WARNING,
    4: logging.ERROR,
    5: logging.CRITICAL
}

###############################################
# Define logger for crawler
###############################################
#fmtstr = " Name: %(user_name)s : %(asctime)s: (%(filename)s): %(levelname)s: %(funcName)s Line: %(lineno)d - %(message)s"
fmtstr = "%(asctime)s:   %(message)s"
datestr = "%m/%d/%Y %I:%M:%S %p "

#basic logging config
logging.basicConfig(
    filename="custom_crawler_output.log",
    filemode="w",
    format=fmtstr,
    datefmt=datestr,
)
# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.WARNING)

c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

crawler_logger = logging.getLogger('crawler')

crawler_logger.addHandler(f_handler)
crawler_logger.addHandler(c_handler)


###############################################
# Define logger for web fuzzer
###############################################
