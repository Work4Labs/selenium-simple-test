from selenium import webdriver
import hmac
from hashlib import md5
import re
import requests
import base64
import json

SAUCELABS_DOMAIN = "saucelabs.com"
SAUCELABS_CONNECTOR_PATH = "ondemand.saucelabs.com:80/wd/hub"
SAUCELABS_REST_PATH = "/rest/v1"


class SauceLabsDriver(webdriver.Remote):

    def __init__(self, command_executor=None, desired_capabilities=None):
        # Extract username and acces_key from the connector url
        regexp = re.compile(r"^https?:\/\/([0-9a-z_]+):([0-9a-z-]+)@.*$")
        match = regexp.search(command_executor)
        try:
            self.username = match.group(1)
            self.access_key = match.group(2)
        except AttributeError:
            raise Exception('Invalid command_executor: %s' % command_executor)

        self.basic_auth = base64.encodestring(
            '%s:%s' % (self.username, self.access_key))[:-1]

        default_capabilities = {
            'record-video': 'false',
            'max-duration': '240'
        }

        # Extend the default capabilities with the custom ones
        default_capabilities.update(desired_capabilities)

        super(SauceLabsDriver, self).__init__(
            desired_capabilities=default_capabilities,
            command_executor=command_executor
        )

    def get_job_result_url(self):
        token = hmac.new('%s:%s' % (self.username, self.access_key),
                         self.session_id,
                         md5).hexdigest()
        return 'https://%s/jobs/%s?auth=%s' % (SAUCELABS_DOMAIN,
                                               self.session_id,
                                               token)

    def job_read(self, job_id):
        result = self._call_rest(
            'GET',
            '/jobs/%s' % job_id
        )
        if result:
            return result.text
        return None

    def job_update(self, result, exception=None):
        data = {
            'public': 'false',
            'passed': result
        }
        if exception:
            data['custom-data'] = {'error' : str(exception)}
        data = json.dumps(data)

        result = self._call_rest(
            'PUT',
            '/jobs/%s' % self.session_id,
            data
        )
        return result.status_code == requests.codes.ok

    def job_list(self, result):
        result = self._call_rest(
            'GET',
            '/jobs'
        )
        if result:
            return result.text
        return None

    def _get_ondemand_url(self):
        return 'http://%s:%s@%s' % (self.username, self.access_key,
                                    SAUCELABS_CONNECTOR_PATH)

    def _get_rest_url(self):
        return 'http://%s/%s/%s' % (SAUCELABS_DOMAIN, SAUCELABS_REST_PATH,
                                    self.username)

    def _call_rest(self, method, path, data=None):
        url = self._get_rest_url() + '/' + path

        try:
            result = getattr(requests, method.lower())(
                url,
                data=data,
                headers={"Authorization": "Basic %s" % self.basic_auth}
            )
            return result
        except Exception:
            # TODO: log something?
            return None
