from __future__ import annotations
import time
from typing import Optional
from pathlib import Path
import os

from flask import Flask, render_template, send_file, request, abort

from ..deserializer import ingest
from .scheduling import add_search, start_work_thread, SEARCHES



app = Flask(__name__)
start_work_thread()


def get_component_abstractions(comp) -> dict[str, str]:
    if hasattr(comp, "ABSTRACTIONS"):
        d = {"99": "-"} | dict((str(level), abs_obj.__class__.__name__) for level, abs_obj in comp.ABSTRACTIONS.items())
        return d
    return {}


# my dumb JSON serializer
def json_serialize(obj) -> int | str | bool | list | dict:
    if isinstance(obj, dict):
        return dict((k, json_serialize(v)) for k, v in obj.items())
    elif isinstance(obj, (tuple, list)):
        return [json_serialize(item) for item in obj]
    elif isinstance(obj, (int, str, bool)):
        return obj
    elif obj is None:
        return "None"
    else:
        # object
        if hasattr(obj, "to_json_dict") and callable(obj.to_json_dict):
            return json_serialize(obj.to_json_dict())
        elif hasattr(obj, "__slot__"):
            d = {}
            for attr in obj.__slot__:
                d[attr] = json_serialize(getattr(obj, attr))
            return d
        else:
            return repr(obj)


@app.route('/')
def index():
    return render_template("index.html", cpvs=CPVS, blueprints=blueprints)


@app.route("/api/cpv_info")
def cpv_info():
    cls_name = request.args.get("name")

    if not cls_name:
        return {"error": "Name is required"}

    for cpv in CPVS:
        if cpv.__class__.__name__ == cls_name:
            break
    else:
        return {"error": "CPV not found"}

    return {
        "name": cpv.NAME,
        "cls_name": cpv.__class__.__name__,
        "components": [
            {
                "name": comp.name,
                "abstractions": get_component_abstractions(comp),
            } for comp in cpv.required_components
        ],
    }

def lookup_blueprint(raw):
    try:
        blueprint_id = int(raw)
        if blueprint_id >= len(blueprints):
            return None
        return blueprints[blueprint_id]
    except (TypeError, ValueError):
        return None

@app.post("/api/ingest_blueprint")
def ingest_blueprint():
    if "name" not in request.args:
        return {"error": "must give name argument"}, 400
    name = request.args["name"]
    if name in blueprints:
        return {"error": "exists"}, 400
    force = request.args.get("force", False)
    serialized = request.get_json(silent=True)
    if serialized is None:
        return {"error": "must give json body"}, 400
    try:
        # TODO: move this to another thread and return a promise?
        ingest(serialized, INGESTION_DIR / name, force=force)
    except FileExistsError as e:
        return {"error": "exists"}, 400
    except ValueError as e:
        return {"error": "couldn't deserialize blueprint"}, 400
    return {}

@app.route("/api/get_blueprint")
def get_blueprint():
    blueprint_id = request.args.get("id", None)

    if blueprint_id not in blueprints:
        return {"error": "Blueprint not found"}
    cps = blueprints[blueprint_id]

    d = {
        "nodes": [],
        "links": [],
        "options": {},
    }
    for node in cps.component_graph:
        d["nodes"].append({"id": id(node), "name": repr(node)})
    for src, dst in cps.component_graph.edges:
        d["links"].append({
            "source": id(src),
            "target": id(dst),
        })
    for option in cps.options:
        d["options"][option] = cps.get_option(option)
    return {
        "component_graph": d
    }

@app.post("/api/set_blueprint_option")
def set_blueprint_option():
    blueprint_id = request.args.get("id", None)

    if blueprint_id not in blueprints:
        return {"error": "Blueprint not found"}
    cps = blueprints[blueprint_id]

    option = request.args.get("option", None)
    value = request.get_json()

    cps.set_option(option, value)
    print(cps.steering.has_aps)

    return {}

@app.route("/api/cpv_search")
def cpv_search():
    # TODO: Getting the components from the front end

    cpv_name = request.args.get("cpv_name", None)
    if cpv_name is None:
        return {"error": "CPV name must be provided"}

    blueprint_id = request.args.get("blueprint_id", None)
    if blueprint_id not in blueprints:
        return {"error": "Blueprint not found"}
    cps = blueprints[blueprint_id]

    # TODO: watch out for thread safety with this cps reference...
    search_id = add_search(cpv=cpv_name, cps=cps)

    return {
        "search_id": search_id,
    }


@app.route("/api/cpv_search_ids")
def cpv_search_ids():

    ids = list(SEARCHES)

    return {
        "ids": ids,
    }


@app.route("/api/cpv_search_result")
def cpv_search_result():
    search_id = request.args.get("id", None)

    if search_id is None:
        return {
            "error": "Search ID cannot be None",
        }

    try:
        search = SEARCHES.get(int(search_id), None)
    except TypeError:
        search = None

    if search is None:
        return {
            "error": "Search not found"
        }

    result = {
        "taken": search.get("taken", False),
        "result": search.get("result", None),
        # "identified_cpv_and_paths": search.get("identified_cpv_and_paths", None),
        "cpv_inputs": search.get("cpv_inputs", None),
        "last_updated": search.get("last_updated", int(time.time() * 10000)),
    }

    return json_serialize(result)


@app.route("/index.js")
def js():
    # TODO: Serve it as a static file
    return send_file("templates/index.js")


# delayed import
from saci_db.devices import devices, ingested
from saci_db.cpvs import CPVS

if (dirname := os.getenv("INGESTION_DIR")) is not None:
    INGESTION_DIR = Path(dirname)
else:
    INGESTION_DIR = Path(ingested.__file__).resolve().parent
del dirname

blueprints = devices | ingested.devices
