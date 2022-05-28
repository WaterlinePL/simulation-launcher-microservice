from flask import Flask, request
from strenum import StrEnum

import kubernetes_job_operator
from redis_operator import RedisOperator

app = Flask(__name__)
redis_operator = RedisOperator("URL:PORT")  # TODO: Get from variable


class RestMethod(StrEnum):
    GET = 'GET'
    DELETE = 'DELETE'
    PUT = 'PUT'
    POST = 'POST'


@app.route("/project-files", methods=[RestMethod.POST, RestMethod.DELETE])
def manage_project_files():
    project_name = request.json["project_name"]
    if request.method == RestMethod.POST:
        return kubernetes_job_operator.create_file_download_job(project_name)
    elif request.method == RestMethod.DELETE:
        return kubernetes_job_operator.create_file_removal_job(project_name)


@app.route("/jobs/hydrus", methods=[RestMethod.POST])
def launch_hydrus():
    project_name = request.json["project_name"]
    model = request.json["model"]
    return kubernetes_job_operator.create_hydrus_job(project_name, model)


@app.route("/jobs/modflow", methods=[RestMethod.POST])
def launch_modflow():
    project_name = request.json["project_name"]
    model = request.json["model"]
    return kubernetes_job_operator.create_modflow_job(project_name, model)


@app.route("/jobs/<job_id>", methods=[RestMethod.GET])
def get_simulation_job_status(job_id: str):
    return redis_operator.get_job_status(job_id)


if __name__ == '__main__':
    # run flask app
    app.run(debug=True, host="0.0.0.0", port=7777)
