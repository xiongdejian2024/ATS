#!/usr/bin/python3
import sys
import logging
import getopt

def setup_logger(level, name):
    logger = logging.getLogger(name)

    try:
        logging._checkLevel(level.upper())
        level = logging.getLevelName(level.upper())
    except ValueError:
        print("ERROR: Invalid debug level (%s) defaulting to WARNING" % level)
        level = logging.WARNING

    logger.setLevel(level)
    if not logger.hasHandlers():
        # create console handler so that we see the assertion errors in the same order as the log.
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        # create formatter and add it to the handler(s).
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s (%(filename)s:%(lineno)d) %(message)s')
        ch.setFormatter(formatter)
        # add the handler(s) to the logger
        logger.addHandler(ch)
    return logger

def printHelp():
    '''
    @brief: Prints the help for parameters
    @return: None
    '''
    print("Usage: logger.py <options>")
    print("    -d --debug = Show debug information, Options: info, debug, warning, error , Default = warning")
    print("    -h --help = Show this help menu")
    return

def main(argv):
    debug = "warning"
    name = "no_name"
    try:
        opts, args = getopt.getopt(argv, "n:d:h", ["name=", "debug="])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            return 0
        elif opt in ("-d", "--debug"):
            debug = arg
        elif opt in ("-n", "--name"):
            name = arg
        else:
            print("Invalid option", opt)
            printHelp()
            return 0
    logger = setup_logger(debug.upper(), name)

    logger.info("Hello world")
    logger.error("Hello world")
    logger.warning("Hello world")
    logger.debug("Hello world")
    return 0
# --------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    result = main(sys.argv[1:])
    sys.exit(result)
