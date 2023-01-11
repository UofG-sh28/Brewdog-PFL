# This script will revert the local default database to the testdb containing test objects.

import os, shutil
if os.path.exists("db.sqlite3"):
    os.remove("db.sqlite3")

try:
    shutil.copy("testdb.sqlite3", "db.sqlite3")
except:
    print("Reset failed, please try again.")
