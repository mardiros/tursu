#!/usr/bin/env python3
import datetime

import tursu

header = (
    f"{tursu.__version__} - "
    f"Released on {datetime.datetime.now().date().isoformat()}"
)
with open("CHANGELOG.md.new", "w") as changelog:
    changelog.write(f"## {header}")
    changelog.write("\n\n")
    changelog.write("* please write here \n\n")
