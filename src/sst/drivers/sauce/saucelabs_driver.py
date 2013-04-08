from selenium import webdriver
import requests
import base64
import json

SAUCELABS_DOMAIN = "saucelabs.com"
SAUCELABS_CONNECTOR_PATH = "ondemand.saucelabs.com:80/wd/hub"
SAUCELABS_REST_PATH = "/rest/v1"


class SauceLabsClient(webdriver.Remote):

    def __init__(self, username, access_key, desired_capabilities=None):
        self.username = username
        self.access_key = access_key
        self.basic_auth = base64.encodestring('%s:%s' % (username, access_key))[:-1]
        super(SauceLabsClient, self).__init__(
            desired_capabilities=desired_capabilities,
            command_executor=self._get_connector_url()
        )

    def jobs_read(self, job_id):
        result = self._call_rest(
            'GET',
            '/jobs/%s' % job_id
        )
        if result:
            return result.text
        return None

    def jobs_update(self, result):
        data = json.dumps({
            'public': 'false',
            'passed': result
        })

        result = self._call_rest(
            'PUT',
            '/jobs/%s' % self.driver.session_id,
            data
        )
        return result.status_code == requests.codes.ok

    def jobs_list(self, result):
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
