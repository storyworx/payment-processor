"""
Settings should always be initialized in __init__
function to prevent multiple calls to config server
"""

import os

from dotenv import load_dotenv

load_dotenv(override=False)

if os.environ["RELEASE_STAGE"] == "dev":
    from conf.dev.settings import *
elif os.environ["RELEASE_STAGE"] == "prod":
    from conf.dev.settings import *
