#!/usr/bin/env python
import sys

import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    from mezzanine.utils.conf import real_project_name

    settings_module = "%s.settings" % real_project_name("AIC_site")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
