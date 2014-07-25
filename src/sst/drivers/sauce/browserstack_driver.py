from selenium import webdriver
from requests.auth import HTTPBasicAuth
import logging
import re
import requests
import base64
import json


class BrowserStackDriver(webdriver.Remote):

    def __init__(self, command_executor=None, desired_capabilities=None):
        # Extract username and acces_key from the connector url
        regexp = re.compile(r"^https?:\/\/([0-9a-z_]+):([0-9a-zA-Z-]+)@.*$")
        match = regexp.search(command_executor)
        try:
            self.username = match.group(1)
            self.access_key = match.group(2)
        except AttributeError:
            raise Exception('Invalid command_executor: %s' % command_executor)

        default_capabilities = {
            'record-video': 'false',
            'max-duration': '240'
        }

        # Extend the default capabilities with the custom ones
        default_capabilities.update(desired_capabilities)

        super(BrowserStackDriver, self).__init__(
            desired_capabilities=default_capabilities,
            command_executor=command_executor
        )

    def get_job_result_url(self):
        r = requests.get(self._get_rest_url(), auth=HTTPBasicAuth(self.username, self.access_key))
        return r.json()['automation_session']['browser_url']

    def job_read(self, job_id):
        result = self._call_rest(
            'GET',
            '/jobs/%s' % job_id
        )
        if result:
            return result.text
        return None

    def job_update(self, result, exception=None):
        data = {'status':'completed'}
        if exception:
            data = {'status':'error'}
        data = json.dumps(data)

        result = self._call_rest(
            'put',
            self._get_rest_url(),
            data,
            headers={'content-type': 'application/json'}
        )
        return result

    def job_list(self, result):
        result = self._call_rest(
            'GET',
            '/jobs'
        )
        if result:
            return result.text
        return None

    def _get_rest_url(self):
        return 'https://www.browserstack.com/automate/sessions/%s.json' % self.session_id

    def _call_rest(self, method, url, data=None, headers=None):
        try:
            r = getattr(requests, method.lower())(url, data=data, headers=headers, auth=HTTPBasicAuth(self.username, self.access_key))
            return r.status_code == requests.codes.ok
        except Exception as e:
            logging.error(e)
            return None
