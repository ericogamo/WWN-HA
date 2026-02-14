import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

_LOGGER = logging.getLogger(__name__)


class WWPortalConnector:
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._session = requests.Session()
        self._session.headers.update(
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) HomeAssistant/WW-Integration",
                "Accept": "application/json, text/plain, */*",
            }
        )

    def login(self):
        """
        Logs in to the portal and establishes a session.
        """
        dashboard_url = "https://www.ww-kundenportal.com/platform/home-portal/dashboard"

        try:
            r = self._session.get(dashboard_url, timeout=30)
            if "auth" in r.url or "login" in r.url:
                soup = BeautifulSoup(r.text, "html.parser")
                form = soup.find("form")
                if not form:
                    _LOGGER.error("Login form not found on page")
                    return False

                action = form.get("action")
                inputs = form.find_all("input")
                payload = {}
                for tag in inputs:
                    name = tag.get("name")
                    value = tag.get("value", "")
                    if name == "username":
                        payload[name] = self._username
                    elif name == "password":
                        payload[name] = self._password
                    elif name:
                        payload[name] = value

                r_login = self._session.post(action, data=payload, timeout=30)
                if r_login.status_code != 200 or "login-actions" in r_login.url:
                    _LOGGER.error("Login failed. Check credentials.")
                    return False

                if "dashboard" in r_login.url or r_login.url == dashboard_url:
                    return True
                else:
                    if r_login.history:
                        return True
                    _LOGGER.error(f"Unexpected redirect after login: {r_login.url}")
                    return False
            else:
                return True  # Already logged in
        except Exception as e:
            _LOGGER.error(f"Error during login: {e}")
            return False

    def fetch_data(self):
        """
        Fetches meter data from the internal API.
        """
        if not self.login():
            return None

        url = "https://www.ww-kundenportal.com/rest/secure/meters"
        try:
            r = self._session.get(url, timeout=30)
            if r.status_code != 200:
                _LOGGER.error(f"API Error {r.status_code}: {r.text}")
                return None

            meters_data = r.json()
            output = {}

            for meter in meters_data:
                m_type = meter.get("meteringType", "")
                mp_number = meter.get("meteringPointNumber", "")
                readings = meter.get("readings", [])

                if readings and isinstance(readings, list):
                    readings.sort(key=lambda x: x.get("timestamp", 0))
                    latest = readings[-1]
                    value = latest.get("value")
                    ts = latest.get("timestamp")  # Unix ms

                    if m_type == "PURCHASE":
                        output["reading_purchase_kwh"] = value
                        output["timestamp_purchase"] = ts
                        output["meter_id_purchase"] = mp_number
                    elif m_type == "FEED_IN":
                        output["reading_feed_in_kwh"] = value
                        output["timestamp_feed_in"] = ts
                        output["meter_id_feed_in"] = mp_number

            return output

        except Exception as e:
            _LOGGER.error(f"Error fetching data: {e}")
            return None
