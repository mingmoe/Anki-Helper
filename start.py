
import papermill as pm
import os
import nbformat
import json
import os
import sys
import shared

# prepare
nb = nbformat.read(open(shared.fsrs4anki_notebook_file,encoding="utf-8"), as_version=4)
shared.logger.info(f"load optimizer from {shared.fsrs4anki_notebook_file}")
config = {}

with open(shared.config_json_file,encoding="utf-8") as f:
    config = json.load(f)

files = []
outputs = []

for f in os.listdir(shared.temp_folder):
    if os.path.isfile(os.path.join(shared.temp_folder,f)) and f.endswith(".apkg"):
        files.append(os.path.join(shared.temp_folder,f))
        shared.logger.info(f"found file:{f}")

# begin to process each file
for f in files:
    # change to
    # because fsrs4 will use its self python module and has a specific path
    os.chdir(shared.fsrs4_folder)

    shared.logger.info(f"process file:{f}")
    pm.execute_notebook(
    nb,
    None,
    parameters=dict(ming_data_file=f,
                    ming_next_day_start=config['next_day_starts_at'],
                    ming_output_file=shared.output_json_file,
                    # Always set this to true. It depend on my person.
                    ming_filter_out_suspended_cards=True)
    )

    #exit
    os.chdir(shared.root_dir)

    with open(shared.output_json_file,encoding="utf-8") as fp:
        name = str(os.path.basename(f)).replace("__","::").replace(".apkg","")
        w = json.load(fp)['w']
        outputs.append({ "w":w,"name":name})

        shared.logger.info(f"done for file:{f} --> as {name} w:{w}")

        if name == config[shared.globalDeck]:
            outputs.append({"w":w,"name":shared.globalDeck})
            shared.logger.info(f"FSRS4:use {name} as {shared.globalDeck}")

shared.logger.info("done all files")
with open(shared.totall_json_file,encoding="utf-8",mode="w") as fp:
    json.dump({"all":outputs},fp=fp)
