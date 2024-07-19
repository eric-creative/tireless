import logging
from pathlib import Path

import click
import os

from tireless.helper import node_init, run_installations, collect_static_files, starter_template
from tireless.inputs import tailwindcss_config_file_content, app_file_content

BASE_DIR = Path.cwd()


@click.group()
def cli() -> None:
    pass


@cli.command()
def init():
    package_json_file = BASE_DIR / "package.json"
    static = BASE_DIR / 'static'
    templates = BASE_DIR / 'templates'
    pages = BASE_DIR / 'pages'
    app_wsgi = BASE_DIR / 'app.py'

    if not os.path.exists(package_json_file):
        logging.info('Tireless initialization started...')
        initialization = node_init()
        if initialization:
            installations = run_installations()
            if installations:
                logging.info("Initialization complete")
                if not os.path.exists(static):
                    collected = collect_static_files(static, templates)
                    if collected:
                        logging.info("Collected static files")

                        # Writing the tailwindcss config file
                        with open(BASE_DIR / "tailwind.config.js", "w+") as f:
                            f.write(tailwindcss_config_file_content)

                        # Writing the app file
                        with open(app_wsgi, "w+") as f:
                            f.write(app_file_content)

                        # Starter template installation
                        installing_starter_template = starter_template(
                            template_dir=templates, static_dir=static, pages_dir=pages
                        )
                        if installing_starter_template:
                            logging.info(f"Starter template was installed")
                        else:
                            logging.warning(f"No starter template was installed, you can create one. see our docs")

                    else:
                        logging.warning("Failed to correct static files")
                else:
                    logging.warning("Failed to collect static files")
            else:
                logging.warning("Initialization tailwindcss failed")
        else:
            logging.warning("Javascript failed to initialize the app")
    else:
        logging.warning("Tailwindcss already installed")
