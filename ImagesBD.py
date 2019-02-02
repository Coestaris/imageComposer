import sys
import logging

import lib.language

defaultLang = "en"

logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_l_value(key):
    return lib.language.getLang(defaultLang)[key]


def print_help(argv):
    print(get_l_value("help"))


def info(argv):
    pass


def main():
    arguments = sys.argv

    if len(arguments) < 2:
        logger.error(get_l_value("err_noargs"))
        return 1

    action = sys.argv[1]
    if action == "create":
        pass
    elif action == "clear":
        pass
    elif action == "help":
        print_help(sys.argv)

    elif action == "info":
        info(sys.argv)
    else:
        logger.error(get_l_value("err_unknown_command").format(action))
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
