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
            "progress": "Progress:",
            "complete": "Complete [%i / %i]",
            "done" : "Done!"
        }
    }
]


def getLang(lang):
    for l in languages:
        if l["lang"] == lang:
            return l["data"]