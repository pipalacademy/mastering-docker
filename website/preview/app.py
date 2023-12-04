from flask import Flask, render_template, send_from_directory, jsonify
from pathlib import Path
import ipytail
import glob
import config

app = Flask(__name__)

notebook_name = config.notebook
notebook_pattern = f"/home/jupyter-*/data-analysis/{notebook_name}"

def get_notebook_path(name):
    return f"/home/jupyter-{name}/data-analysis/{notebook_name}"

def get_name(path):
    path = Path(path)
    return path.parent.parent.name.replace("jupyter-", "")

@app.route("/")
def index():
    paths = glob.glob(notebook_pattern)
    names = sorted(get_name(path) for path in paths)
    return render_template("index.html", notebooks=names)

@app.route("/nb/<name>.ipynb")
def notebook_ipynb(name):
    path = Path(get_notebook_path(name))
    return send_from_directory(path.parent, path.name)


@app.route("/nbtail/<name>.ipynb")
def notebook_tail(name):
    path = get_notebook_path(name)

    tail = ipytail.IPyTail()
    nb = tail.process_file(path, skip_till=config.header, tail=False)

    nb = dict(nb, cells=nb['cells'][config.skip_cells:][:config.num_cells])

    return jsonify(nb)

@app.route("/nb/<name>")
def notebook(name):
    return render_template("notebook.html",
                           name=name)

if __name__ == "__main__":
    app.run()
