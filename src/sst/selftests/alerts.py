from sst.actions import *

goto('/alerts')

# Accept an alert box and assert its text.
button_click('show-alert', wait=False)
alert_accept(u'JavaScript alert text')
title_is('Page with JavaScript alerts')

# Accept a confirm box.
button_click('show-confirm', wait=False)
alert_accept()
alert_accept(u'Confirm accepted')

# Dismiss a confirm box and assert its text.
button_click('show-confirm', wait=False)
alert_dismiss(u'JavaScript confirm text')
alert_accept(u'Confirm dismissed')

# Enter text to a prompt box, accept it and assert its text.
button_click('show-prompt', wait=False)
alert_accept(u'JavaScript prompt text', 'Entered text')
alert_accept('Entered text')

# Enter text to a prompt box and dismiss it.
button_click('show-prompt', wait=False)
alert_dismiss(text_to_write='Entered text')
title_is('Page with JavaScript alerts')
