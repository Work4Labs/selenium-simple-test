JAVASCRIPT_DISABLED = True

from sst.actions import browser

profile = browser.firefox_profile
javascript_enabled = profile.default_preferences['javascript.enabled']

assert javascript_enabled == 'false'
