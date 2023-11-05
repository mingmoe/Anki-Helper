
import json
import os
import sys
import shared
import difflib

# prepare
text = ""
total = {}

with open(shared.totall_json_file,encoding="utf-8") as f:
    total = json.load(f)['all']

with open(shared.fsrs4anki_scheduler_js_file,encoding="utf-8") as f:
    text = f.read()

configStartIndex = text.find(shared.configStart)
configEndIndex = text.find(shared.configEnd)

if configStartIndex == -1 or configEndIndex == -1:
    shared.logger.error("couldn't found the Configuration comment!")
    sys.exit(1)

def replaceConfig(config:str):
    fi :int = (configStartIndex + len(shared.configStart))
    si :int = configEndIndex
    return text[0:fi] + "\n\n" + config + "\n\n" + text[si:]

config : str = ""

# gen deckParams
deck_params = "const deckParams = [\n"

for item in total:
    param = """
    {
    "deckName": "A DECK HERE",
    "w": A W HERE,
    "requestRetention": 0.9,
    "maximumInterval": 36500,
    "easyBonus": 1.3,
    "hardInterval": 1.2,
    },"""
    param = param.replace("A DECK HERE", str(item["name"]))
    param = param.replace("A W HERE", str(item["w"]))
    deck_params += param
    deck_params += "\n"

# remove last \n and ,
deck_params = deck_params[:-2]
deck_params += "\n];"

config += deck_params

# some defulat options
config += """
// To turn off FSRS in specific decks, fill them into the skip_decks list below.
// And add <div id=deck deck_name="{{Deck}}"></div> to your card's front template's first line.
// Please don't remove it even if you don't need it.
const skip_decks = [];

// "Fuzz" is a small random delay applied to new intervals to prevent cards from
// sticking together and always coming up for review on the same day
const enable_fuzz = true;

// FSRS supports displaying memory states of cards.
// Enable it for debugging if you encounter something wrong.
const display_memory_state = false;
"""

# as a result
result = replaceConfig(config)
shared.logger.info("gen scheduler done")
with open("scheduler.js",mode="r+",encoding="utf-8") as f:
    got = f.read()

    f.truncate(0)
    f.seek(0)
    f.write(result)

    diffs = difflib.ndiff(got.splitlines(keepends=True),result.splitlines(keepends=True))

    for diff in diffs:
        if not diff.startswith(" "):
            print(diff)
