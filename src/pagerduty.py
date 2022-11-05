import re
from enum import Enum

import requests
from local_settings import *


class PagerDutyUrgency(Enum):
	URGENCY_HIGH = "high"
	URGENCY_LOW = "low"

class PagerDutyAlert(object):
	@classmethod
	def sendPagerDutyRequest(cls, method, endpoint, payload):
		headers = {
			"Authorization": f"Token token={PAGERDUTY_APIKEY}",
			"Accept": "application/vnd.pagerduty+json;version=2",
			"Content-Type": "application/json",
			"From": "ideasparkhk@outlook.com",
		}
		if method == "GET":
			return requests.get(endpoint, params=payload, headers=headers)
		elif method == "POST":
			return requests.post(endpoint, json=payload, headers=headers)
		elif method == "PUT":
			return requests.put(endpoint, json=payload, headers=headers)

	@classmethod
	def sendPagerDutyAlert(cls, service_id: str, incident_key: str, urgency: PagerDutyUrgency, title: str, body: str = ""):
		payload = {
			"incident": {
				"type": "incident",
				"title": title,
				"service": {
					"id": service_id,
					"type": "service_reference",
				},
				"urgency": urgency.value,
				"body": {
					"type": "incident_body",
					"details": body,
				},
				"incident_key": incident_key,
			}
		}
		return cls.sendPagerDutyRequest("POST", "https://api.pagerduty.com/incidents", payload)

	@classmethod
	def listPagerDutyAlert(cls, service_id: str, status: str, offset: int = 0, limit: int = 25):
		payload = {
			"service_ids[]": service_id,
			"statuses[]": status,
			"offset": offset,
			"limit": limit,
		}
		return cls.sendPagerDutyRequest("GET", "https://api.pagerduty.com/incidents", payload)

	@classmethod
	def resolvePagerDutyAlert(cls, incident_id: str):
		payload = {
			"incident": {
				"type": "incident_reference",
				"status": "resolved",
			}
		}
		return cls.sendPagerDutyRequest("PUT", f"https://api.pagerduty.com/incidents/{incident_id}", payload)


class PagerDutyHelper(object):
	@classmethod
	def getIncidents(cls, service_id: str, conditional_regex: str):
		incidents = []
		for status in ["triggered", "acknowledged"]:
			offset = 0
			while True:
				resp = PagerDutyAlert.listPagerDutyAlert(service_id, status=status, offset=offset).json()
				for incident in resp["incidents"]:
					if incident["incident_key"] and re.match(conditional_regex, incident["incident_key"]):
						incidents.append(incident)
				if resp["more"] is False:
					break
				else:
					offset += int(resp["limit"])

		return incidents
