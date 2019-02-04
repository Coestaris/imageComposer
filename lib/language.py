languages = [
    {
        "lang": "en",
        "data": {
            "err_noargs": "You must specify some arguments",
            "err_unknown_command": "\"{}\" is unknown command. Use \"help\" to get list of commands",
            "help": """Actions list:
1. 
2. 
3.""",
            "progress": "Process-%i:",
            "complete": "Complete [%i / %i]",
            "done_in": "Done! (in %i seconds)",
            "done": "Done!",
            "del_conf": "Are you sure you want to delete all database? [y/n]: ",
            "aborted": "Aborted!",

            "warn_db_exists": "Warning! Some database already exists. It may be overlapped",
            "err_specify_img": "You must specify some image to compare with DB (img=<some filename>)",
            "err_file_not_exists": "Specified file \"%s\" doesnt exist",
            "hash_diff": "%s: %3.2f difference"
        }
    }
]


def getLang(lang):
    for l in languages:
        if l["lang"] == lang:
            return l["data"]