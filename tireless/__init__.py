import logging
import signal
import subprocess
import threading

from flask import Flask
from tireless.cli import BASE_DIR

template_dir = BASE_DIR / 'templates'
static_dir = BASE_DIR / 'static'
db_dir = BASE_DIR / 'database.db'
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_dir)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


def run_tailwindcss_server(stop_event):
    # Run the Tailwind CSS server
    cmd = [
        "npx.cmd",
        "tailwindcss",
        "-i",
        str(template_dir / "global.css"),
        "-o",
        str(static_dir / "css/styles.css"),
        "--watch",
    ]

    # print("Running Tailwind CSS server...")
    p = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    while not stop_event.is_set():
        p.poll()
        if p.returncode is not None:
            print("Tailwind CSS server stopped.")
            break
        stop_event.wait(1)
        if p.returncode is None:
            continue

    if p.returncode is None:
        # print("Terminating Tailwind CSS server...")
        p.terminate()
        p.wait()
        print("Tailwind CSS server terminated.")


def run(debug):
    stop_event = threading.Event()
    tailwind_thread = threading.Thread(target=run_tailwindcss_server, args=(stop_event,), daemon=True)
    tailwind_thread.start()
    original_handler = signal.getsignal(signal.SIGINT)

    def sigint_handler(signum, frame):
        stop_event.set()

        # wait for tailwind server to stop
        tailwind_thread.join()

        # stop the flask server
        app.logger.info('Stopping server...')
        app.logger.info('Server stopped.')
        original_handler(signum, frame)
        exit(0)

    try:
        signal.signal(signal.SIGINT, sigint_handler)
    except ValueError as e:
        logging.error(f'{e}. Continuing execution...')

    app.run(debug=debug)
