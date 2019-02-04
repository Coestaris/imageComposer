#!/usr/bin/python3

import shutil
import sys
import logging
import glob
import os
import json
import multiprocessing
import time

from time import sleep

import lib.db
import lib.img_processor
import lib.language

defaultLang = "en"

logging.basicConfig(format='[%(asctime)s][%(levelname)s]: %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')


def get_parameters(parameters, argv):
    for index, arg in enumerate(argv, 1):
        for k, v in parameters.items():
            if arg.startswith(k):
                value = arg.split('=')[1]
                parameters[k] = value


def get_l_value(key):
    return lib.language.getLang(defaultLang)[key]


def send(cmd):
    sys.stdout.write(cmd)
    sys.stdout.flush()


def save_cursor():
    send('\033[s')
    # send('\033[s')


def restore_cursor():
    send('\033[u')
    # send('\033[u')


def print_help(argv):
    print(get_l_value("help"))


def chunk_it(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out


def create_thread(files, path, prIndex, shared):
    outpath = path % (multiprocessing.current_process().name + "/%s")

    try:
        os.mkdir(path % multiprocessing.current_process().name)
    except:
        pass

    for index, file in enumerate(files):
        with open(outpath % str(index) + ".json", mode="w+") as f:
            inf = lib.img_processor.get_img_info(files[index], index).to_json()
            json.dump(inf, f)
            shared[prIndex] = index + 1


def create(argv):
    parameters = {
        "input": "input",
        "output": "output",
        "count": "5000",
        "offset": "0",
        "threads": "2",
        "name_frmt": "*",
    }

    get_parameters(parameters, argv)

    input_path = "%s/%s/%s" % (os.getcwd(), parameters["input"], parameters["name_frmt"])
    output_path = "%s/%s/%%s" % (os.getcwd(), parameters["output"])

    files = glob.glob(input_path)

    count = int(parameters["count"])
    offset = int(parameters["offset"])
    thread_count = int(parameters["threads"])

    shared = multiprocessing.Array('i', [0] * thread_count)
    counts = [0] * thread_count

    print(parameters)

    if os.path.isdir(output_path % "Process-1"):
        print(get_l_value("warn_db_exists"))
        print()

    try:
        os.mkdir("%s/%s" % (os.getcwd(), parameters["output"]))
    except:
        pass

    threads = []
    work = chunk_it(files[:count], thread_count)

    for i in range(0, thread_count):
        threads.append(multiprocessing.Process(target=create_thread, args=[work[i], output_path, i, shared]))
        counts[i] = len(work[i])

    for thread in threads:
        thread.start()

    start = time.time()
    save_cursor()
    working = True
    while working:

        working = False
        for index, thread in enumerate(threads):
            if thread.is_alive():
                working = True

            max_progress = counts[index]
            current_progress = shared[index]

            printProgressBar(current_progress, max_progress, prefix=get_l_value("progress") % index,
                             suffix=get_l_value("complete") % (current_progress, max_progress), length=50)

            print()

        restore_cursor()
        sleep(0.3)

    for i in range(0, thread_count):
        print()

    print(get_l_value("done_in") % (time.time() - start))


def info(argv):
    pass


def clear(argv):
    parameters = {
        "output": "output",
    }
    get_parameters(parameters, argv)

    key = input(get_l_value("del_conf"))
    if key in ["y", "Y", "н", "Н"]:

        path = "%s/%s" % (os.getcwd(), parameters["output"])

        if not os.path.isdir(path):
            return 0

        shutil.rmtree(path)
        print(get_l_value("done"))
    else:
        print(get_l_value("aborted"))

    return 0


def compare(argv):
    parameters = {
        "output": "output",
        "input": "input",
        "img": "",
        "threshold": "0",
    }
    get_parameters(parameters, argv)

    threshold = float(parameters["threshold"])

    if parameters["img"] == "":
        logger.error(get_l_value("err_specify_img"))
        return 1

    print(parameters, end='\n\n')

    db_path = "%s/%s" % (os.getcwd(), parameters["output"])
    path = "%s/%s/%s" % (os.getcwd(), parameters["input"], parameters["img"])

    database = lib.db.load(db_path)
    im_info = None

    for info in database:
        if info.path == path:
            im_info = info
            break

    if im_info is None:
        if not os.path.isfile(path):
            logger.error(get_l_value("err_file_not_exists") % path)
            return 1
        info = lib.img_processor.get_img_info(path, -1)

    for info in database:

        diff = lib.img_processor.hash_diff(info.im_hash, im_info.im_hash)
        if threshold != 0:
            if diff[1] < threshold:
                print(get_l_value("hash_diff") % (info.path, diff[1]))

        else:
            print(get_l_value("hash_diff") % (info.path, diff[1]))

    print(get_l_value("done"))
    return 0


def main():
    arguments = sys.argv

    if len(arguments) < 2:
        logger.error(get_l_value("err_noargs"))
        return 1

    action = sys.argv[1]
    if action == "create":
        return create(sys.argv)

    elif action == "clear":
        return clear(sys.argv)

    elif action == "help":
        print_help(sys.argv)

    elif action == "info":
        return info(sys.argv)

    elif action == "compare":
        return compare(sys.argv)

    else:
        logger.error(get_l_value("err_unknown_command").format(action))
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
