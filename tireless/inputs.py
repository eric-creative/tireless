tailwindcss_config_file_content = """/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,j2}"],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
global_css_file_content = """@tailwind base;
@tailwind components;
@tailwind utilities;
"""
layout_jinja2_file_content = """<!doctype html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="{{ url_for('static', filename='css/styles.css') }}" rel="stylesheet">
</head>
    <body>
        {% block content %}{% endblock %}
    </body>
</html>
"""
page_file_template_content = """<!-- page.j2 -->
{% extends "layout.j2" %}

{% block title %}
	Tireless
{% endblock %}

{% block content %}
    <!-- Your specific content for the index page -->
    <h1>Welcome to My Flask App + Tireless</h1>
    <!-- Other content here -->
{% endblock %}

"""
page_file_content = """from flask import Blueprint, render_template
from tireless import app

page = Blueprint('page', __name__, template_folder='templates', static_folder='static')


@app.route('/')
def index():
    return render_template('page.j2')

"""
app_file_content = """from tireless import app
from tireless import run

# import the routes
from pages.page import page

# register the routes
app.register_blueprint(page)

if __name__ == '__main__':
    # run() uncomment this line if you want to run the app in production mode
    run(debug=True)  # comment this line if you want to run the app in production mode

"""