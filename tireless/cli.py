import logging
from pathlib import Path

import click
import os

from tireless.helper import node_init, run_installations, collect_static_files, starter_template, register_blueprints
from tireless.inputs import tailwindcss_config_file_content, app_file_content
from tireless.loader import cook_template, cook_page

BASE_DIR = Path.cwd()

package_json_file = BASE_DIR / "package.json"
static = BASE_DIR / 'static'
templates = BASE_DIR / 'templates'
pages = BASE_DIR / 'pages'
app_wsgi = BASE_DIR / 'app.py'

template_pages_dir = templates / "pages"


@click.group()
def cli() -> None:
    pass


@cli.command('initialize', help='Initialize the project')
def init():
    if not os.path.exists(package_json_file):
        logging.info('Tireless initialization started...')
        initialization = node_init()
        if initialization:
            installations = run_installations()
            if installations:
                logging.info(" Initialization complete")
                if not os.path.exists(static):
                    collected = collect_static_files(static, templates)
                    if collected:
                        logging.info(" Collected static files")

                        # Writing the tailwindcss config file
                        with open(BASE_DIR / "tailwind.config.js", "w+") as f:
                            f.write(tailwindcss_config_file_content)

                        # Writing the app file
                        with open(app_wsgi, "w+") as f:
                            f.write(app_file_content)

                        # Starter templates installation
                        installing_starter_template = starter_template(
                            template_dir=templates, static_dir=static, pages_dir=pages
                        )
                        if installing_starter_template:
                            logging.info(f" Starter template was installed")
                        else:
                            logging.warning(f" No starter template was installed, you can create one. see our docs")

                    else:
                        logging.warning(" Failed to correct static files")
                else:
                    logging.warning(" Failed to collect static files")
            else:
                logging.warning(" Initialization tailwindcss failed")
        else:
            logging.warning(" Javascript failed to initialize the app")
    else:
        logging.warning(" Tailwindcss already installed")


@cli.command(help='Create a new project')
@click.option('-p', '--page', type=str, help='Add new page with no hustle.', required=True)
def add(page: str):
    if not os.path.exists(pages):
        logging.warning(click.style(f" an attempt to create a '{page}' page exited with an error", fg="yellow"))
        logging.error(click.style(
            '" pages" directory does not exist', fg='red'
        ))
    else:

        # cooking new pages and new templates
        page_temp = cook_page(page=page)
        template = cook_template(page=page)

        if os.path.exists(BASE_DIR / "pages" / f"{page}.py"):
            logging.error(click.style(
                f" page '{page}' already exists. Please choose a different page", fg="yellow"
            ))
        else:
            if register_blueprints(app_dir=app_wsgi, page=page, BASE_DIR=BASE_DIR, page_temp=page_temp):
                template_page_dir = template_pages_dir

                # creating respective jinja2 templates for the blueprints
                os.mkdir(template_page_dir / page)
                with open(template_page_dir / page / 'page.j2', "w+",  encoding="utf-8") as f:
                    f.write(template)

                click.echo(
                    click.style(
                        f"|--->>> page {page} was created successful", fg="green"
                    )
                )
            else:
                click.echo(
                    click.style(
                        f"|--->>> page '{page}' could not be created. Please try again", fg="red"
                    )
                )

