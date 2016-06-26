from flask import Flask
from flask import render_template
from flask import request, redirect, url_for, flash
import os
import datetime
import json

import graph as G
import config as CFG
import database as DB

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = CFG.UPLOAD_FOLDER
app.config['SECRET_KEY'] = CFG.SECRET_KEY


@app.route("/", methods=['GET', 'POST'])
def root():
    # Check if empty file index, initialize if True
    DB.init_index()

    file_name = request.values.get('file_name')
    if file_name is not None:
        file_to_show = os.path.join('static', file_name)
    else:
        file_to_show = None

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and CFG.allowed_file(file.filename):
            # Save uploaded file
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)

            # Read graph from file and remove the file
            graph = G.read_excel_graph(filename)
            os.remove(filename)

            # Save graph in d3.js--compatible JSON
            filename = '.'.join(filename.split('.')[:-1]) + '.json'
            G.write_graph_to_json(graph, filename)

            # Update file index file:
            DB.update_index(filename)

            return redirect(url_for('root', file_name=os.path.basename(filename)))

    uploaded_files = DB.read_index()

    return render_template('graph.html',
                           files=uploaded_files,
                           data=file_to_show)


if __name__ == '__main__':
    app.run(host=CFG.APP_HOST,
            port=CFG.APP_PORT,
            debug=CFG.APP_DEBUG)
