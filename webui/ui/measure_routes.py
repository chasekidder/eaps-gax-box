from flask import Blueprint

from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import send_from_directory
from flask import jsonify

from webui import utils
from webui.ui.forms import CycleConfigForm
# from app.measurement.measure import celery, start_cycle


measure_routes = Blueprint("measure_routes", __name__)

@measure_routes.route("/config/", methods=["GET", "POST"])
def config():
    form = CycleConfigForm()

    if request.method == 'POST' and form.validate():
        config = {
            "sample_frequency": form.frequency.data,
            "duration": form.duration.data,
            "sensor_metadata": {
                0: "MPL3115A2",
                1: "TEROS12",
                2: "AWM3300V",
                3: "ABPxxx",
                4: "LOX02F",
                5: "GMP251",
            }
        }

        #task = start_cycle.delay(config)
        #async_result = celery.AsyncResult(id=task.task_id, app=celery)

        # LAUNCH main here!!!!!!!!!!!!!!!!
        
        flash("Success! Configuration sent to box. Measurements Starting...", "alert-success")
        return redirect("/live/")

    elif request.method == 'POST' and not form.validate():
        flash("Required Field Not Completed!", "alert-warning")

    return render_template("config.html", form=form)

@measure_routes.route("/data/")
def data():
    files = utils.get_files_in_dir("/")
    return render_template("data.html", file_list=files)

@measure_routes.route("/download/")
def download_root():
    return render_template("404.html"), 404

@measure_routes.route("/download/<string:file_name>/")
def download(file_name):
    return send_from_directory("/", filename=file_name)

@measure_routes.route("/api/")
def api():
    data = utils.get_live_data()
    return jsonify(data)