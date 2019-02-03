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
            "done": "Done! (in %i seconds)"
        }
    }
]


def getLang(lang):
    for l in languages:
        if l["lang"] == lang:
            return l["data"]