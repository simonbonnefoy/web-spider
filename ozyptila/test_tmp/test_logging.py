import logging


def main():
    #fmtstr = " Name: %(user_name)s : %(asctime)s: (%(filename)s): %(levelname)s: %(funcName)s Line: %(lineno)d - %(message)s"
    fmtstr = " %(asctime)s: (%(filename)s): %(levelname)s: %(funcName)s Line: %(lineno)d - %(message)s"
    datestr = "%m/%d/%Y %I:%M:%S %p "

    #basic logging config
    logging.basicConfig(
        filename="custom_log_output.log",
        level=logging.INFO,
        filemode="w",
        #format=fmtstr,
        #format = '% (name) s - % (levelname) s - % (message) s',
        #format = ' % (message) s',
        #datefmt=datestr,
    )

    logging.info("Info message")
    logging.warning("Warning message")

if __name__ == '__main__':
    main()
