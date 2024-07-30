import os
import jinja2

current_dir = os.path.dirname(__file__)
template_dir = os.path.join(current_dir, 'tir')

env = jinja2.Environment(loader=jinja2.FileSystemLoader(f'{template_dir}'))
page_ = env.get_template('page.j2')


def cook_page(page):
    return page_.render(page=page, url_prefix=f'/{page}')


def cook_template(page):
    return (
        f"<!-- {page}.j2 -->\n"
        """{% extends "layout.j2" %}

        {% block title %}"""
        f"\t{page}"
        """{% endblock %}
    
{% block content %}
    <!-- Your specific content for the index page -->
    <div class="flex h-screen w-full justify-center items-center bg-slate-100">"""
        f'\n\t<h1 class="permanent-marker-regular text-5xl">{page}</h1>\n'
        """\t</div>
    <!-- Other content here -->
{% endblock %}
"""
    )
