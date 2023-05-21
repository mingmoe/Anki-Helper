# ------------------------------------------------------------------------------
#      __init__.py
#      Copyright (C) 2022-now  mingmoe
#
#      This program is free software: you can redistribute it and/or modify
#      it under the terms of the GNU Affero General Public License as
#      published by the Free Software Foundation, either version 3 of the
#      License, or (at your option) any later version.
#
#      This program is distributed in the hope that it will be useful,
#      but WITHOUT ANY WARRANTY; without even the implied warranty of
#      MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#      GNU Affero General Public License for more details.
#
#      You should have received a copy of the GNU Affero General Public License
#      along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
import os
from anki import collection


# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def export_function() -> None:
    opt_dir = QFileDialog.getExistingDirectory(parent=mw, caption="Select a folader to export")

    # get the number of cards in the current collection, which is stored in
    # the main window
    col = mw.col
    all_decks = mw.col.decks.all_names_and_ids()
    # show a message box
    for item in all_decks:
        limit = collection.DeckIdLimit(item.id)
        col.export_anki_package(out_path=os.path.join(opt_dir, item.name.replace("::", "__") + ".apkg"), limit=limit,
                                with_media=False, with_scheduling=True,
                                legacy_support=True)


# create a new menu item, "test"
action = QAction("Export All Decks", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, export_function)

# and add it to the tools menu
mw.form.menuTools.addAction(action)
