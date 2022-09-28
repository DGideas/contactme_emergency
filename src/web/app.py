import csv
import logging
import uuid
from crypt import methods
from typing import Dict

from flask import Flask, render_template, request

from src.pagerduty import PagerDutyAlert, PagerDutyUrgency

logger = logging.getLogger("contactme.app")
logging.basicConfig()
logger.setLevel(logging.INFO)

app = Flask(__name__, template_folder="../templates")

def get_keys() -> Dict[str, str]:
    res = {}
    with open("contact.csv", "r") as _f:
        f = csv.DictReader(_f)
        for line in f:
            res[line["key"]] = line["name"]
    return res

@app.route('/', methods=["GET"])
def do_index():
    key = request.args.get("key", None)
    keys = get_keys()
    if key not in keys:
        return render_template("invalid.htm")
    return render_template('index.htm', your_name=keys[key], your_key=key)

@app.route('/emergency_contact', methods=["POST"])
def do_emergency_contact():
    key = request.form.get("key", None)
    keys = get_keys()
    if key not in keys:
        return render_template("invalid.htm")
    PagerDutyAlert.sendPagerDutyAlert(
        "PKOLAAK",
        str(uuid.uuid4()),
        PagerDutyUrgency.URGENCY_HIGH,
        f"Emergency notification from {keys[key]}",
        f"You should reply {keys[key]} as soon as possible.",
    )
    return {"status": "success"}
