import logging
import os
import shutil
import subprocess

import click

from tireless.inputs import layout_jinja2_file_content, global_css_file_content, page_file_content, \
    page_file_template_content


def node_init():
    cmd_start = [
        "npm.cmd",
        "init",
        "-y",
    ]
    p = subprocess.run(
        cmd_start, shell=True, stdout=subprocess.DEVNULL
    )
    if p.returncode != 0:
        return False
    return True


def run_installations():
    cmd_start = [
        "npm.cmd",
        "install",
        "-D",
        "tailwindcss",
    ]

    cmd_end = [
        "npx.cmd",
        "tailwindcss",
        "init"
    ]

    p = subprocess.run(
        cmd_start, shell=True, stdout=subprocess.DEVNULL
    )
    if p.returncode != 0:
        return False
    else:
        p = subprocess.run(
            cmd_end, shell=True, stdout=subprocess.DEVNULL
        )
        if p.returncode != 0:
            return False
        else:
            logging.info(f"Installed tailwind css")
            return True


def collect_static_files(static, templates):
    css_dir = static / 'css'
    js_dir = static / 'js'

    base_template = templates / 'layout.j2'
    try:

        """make static directory"""
        os.mkdir(static)
        """make templates directory"""
        os.mkdir(templates)

        '''make sub static directory'''
        os.mkdir(css_dir)
        os.mkdir(js_dir)
        '''make sub templates directory'''
        with base_template.open('w') as file:
            file.write("Base templates")

    except FileExistsError:
        raise FileExistsError(f'Static files seems to be collected before')
    else:
        return True


def jinja_starter_template(template_dir):
    # making the page templates
    os.chdir(template_dir)

    page_file = template_dir / 'page.j2'

    with open(page_file, 'w+') as file:
        file.write(page_file_template_content)


def starter_template(template_dir, static_dir, pages_dir):
    # check if the static and templates directory exists
    static_dir_exists = os.path.exists(static_dir)
    template_dir_exists = os.path.exists(template_dir)
    pages_dir_exists = os.path.exists(pages_dir)

    init_file = pages_dir / '__init__.py'
    page_file = pages_dir / 'page.py'

    # If they do not exist the creation
    if static_dir_exists and template_dir_exists:
        global_css_file = template_dir / 'global.css'
        layout_jinja2_file = template_dir / 'layout.j2'

        with open(global_css_file, "w+") as file:
            file.write(global_css_file_content)
            file.close()

        with open(layout_jinja2_file, "w+") as file:
            file.write(layout_jinja2_file_content)
            file.close()

        if pages_dir_exists:
            value = input("We found a pages file, would you like to replace it with the new templates?(y/n) ")

            if value.lower() == 'y' or value.lower() == 'yes':
                """delete the pages dir with all what it contains"""
                shutil.rmtree(pages_dir)
                """Add another pages folder"""
                os.mkdir(pages_dir)
                os.chdir(pages_dir)
                with open(init_file, 'w+') as file:
                    file.write("")
                with open(page_file, 'w+') as file:
                    file.write(page_file_content)
                jinja_starter_template(template_dir)
                return True
            elif value.lower() == 'n' or value.lower() == 'no':
                logging.info(
                    f'Pages folder will not be created, consider reading the documentations to see how to pass')
                return False
            else:
                logging.warning(f"Invalid response {value}")
                return False
        else:
            os.mkdir(pages_dir)
            os.chdir(pages_dir)
            with open(init_file, 'w+') as file:
                file.write("")
            with open(page_file, 'w+') as file:
                file.write(page_file_content)
            jinja_starter_template(template_dir)
            return True

    else:
        logging.warning('Unable to find templates path')


def register_blueprints(app_dir, page, BASE_DIR, page_temp) -> bool | None:
    if os.path.exists(app_dir):
        # click.echo('registering')
        with open(BASE_DIR / 'pages' / f'{page}.py', 'w+') as f:
            f.write(page_temp)
        # register in app.py
        with open(app_dir, 'r+') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                imported = line.startswith(f"from from pages.{page} import bp as {page}")
                if imported:
                    logging.error(f" {page} already registered")
                    return
                else:
                    if line.startswith("from pages.page import bp as page"):
                        lines[i] = line.strip() + f"\nfrom pages.{page} import bp as {page}\n"
                    if line.startswith(f"app.register_blueprint(page)"):
                        lines[i] = line.strip() + f"\napp.register_blueprint({page})\n"

            f.seek(0)
            for line in lines:
                f.write(line)

        return True
    else:
        logging.error(
            click.style(
                f" app.py does not exist", fg='red'
            )
        )
        return False
