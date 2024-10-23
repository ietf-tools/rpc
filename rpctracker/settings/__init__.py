# Copyright The IETF Trust 2024, All Rights Reserved
"""Django settings"""

import os

if os.environ.get("PURPLE_DEPLOYMENT_MODE", "production") == "development":
    from .development import *
else:
    from .production import *
