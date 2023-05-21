
import os
import sys

configStart = "// Configuration Start\n"
configEnd = "// Configuration End\n"

globalDeck = "global config for FSRS4Anki"

root_dir = os.path.abspath(os.getcwd())
temp_folder = os.path.join(root_dir,"temp")

fsrs4_folder = os.path.join(root_dir,"fsrs4anki")
fsrs4anki_scheduler_js_file = os.path.join(fsrs4_folder,"fsrs4anki_scheduler.js")
fsrs4anki_notebook_file = os.path.join(fsrs4_folder,"fsrs4anki_optimizer.ipynb")

output_json_file = os.path.join(root_dir,"output.json")
totall_json_file = os.path.join(root_dir,"total.json")
config_json_file = os.path.join(root_dir,"config.json")

from loguru import logger as priv_logger

priv_logger.add(sys.stdout, colorize=True, format="<green>{time}</green> {level}  <level>{message}</level>")

logger = priv_logger
