import sys
import logging
import glob
import os
import json

import lib.img_processor
import lib.language

defaultLang = "en"

logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    """'
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()


def get_parameters(parameters, argv):
    for index, arg in enumerate(argv, 1):
        for k, v in parameters.items():
            if arg.startswith(k):
                value = arg.split('=')[1]
                parameters[k] = value


def get_l_value(key):
    return lib.language.getLang(defaultLang)[key]


def print_help(argv):
    print(get_l_value("help"))


def create(argv):
    parameters = {
        "input": "input",
        "output": "output",
        "count": "5000",
        "offset": "0",
        "name_frmt": "*",
    }
    get_parameters(parameters, argv)

    input_path = "%s/%s/%s" % (os.getcwd(), parameters["input"], parameters["name_frmt"])
    output_path = "%s/%s/%%s.json" % (os.getcwd(), parameters["output"])

    files = glob.glob(input_path)
    count = int(parameters["count"])
    offset = int(parameters["offset"])

    print(parameters)

    try:
        os.mkdir("%s/%s" % (os.getcwd(), parameters["output"]))
    except:
        pass

    printProgressBar(0, count, prefix='', suffix=get_l_value("complete") % (0, count), length=50)
    for index, file in enumerate(files, offset):
        if index < count + offset:
            with open(output_path % (index + offset), mode="w+") as f:
                inf = lib.img_processor.get_img_info(files[index], index + offset).to_json()

                json.dump(inf, f)
                printProgressBar(index - offset + 1, count, prefix=get_l_value("progress"),
                                 suffix=get_l_value("complete") % (index + 1, count), length=50)
        else:
            break

    print(get_l_value("done"))

def info(argv):
    pass


def main():
    arguments = sys.argv

    if len(arguments) < 2:
        logger.error(get_l_value("err_noargs"))
        return 1

    action = sys.argv[1]
    if action == "create":
        return create(sys.argv)

    elif action == "clear":
        pass
    elif action == "help":
        print_help(sys.argv)

    elif action == "info":
        return info(sys.argv)

    else:
        logger.error(get_l_value("err_unknown_command").format(action))
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
