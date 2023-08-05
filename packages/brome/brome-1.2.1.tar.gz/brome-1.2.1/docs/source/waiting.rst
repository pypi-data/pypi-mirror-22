Waiting For Elements
====================

Waiting methods
---------------

Use the `proxy_driver` (`pdriver`) to wait for element to be clickable, present, not present, visible or not visible::

    pdriver.wait_until_clickable("xp://*[contains(@class, 'button')])

    pdriver.wait_until_present("cn:test")

    pdriver.wait_until_not_present("sv:submit_button")

    pdriver.wait_until_visible("tn:div")

    pdriver.wait_until_not_visible("cs:div > span")

Kwargs and config
#################

All the waiting methods accept the two following kwargs:

* `timeout` (int) second before a timeout exception is raise
* `raise_exception` (bool) raise an exception or return a bool

The config default for these kwargs are respectively:

* `proxy_driver:default_timeout`
* `proxy_driver:raise_exception`

Examples
########

::

    pdriver.wait_until_clickable("xp://*[contains(@class, 'button')]", timeout = 30)

    pdriver.wait_until_present("cn:test", raise_exception = True)

Not waiting methods
-------------------

Use the `proxy_driver` (`pdriver`) to find out if an element is present or visible::

    pdriver.is_visible("xp://*[contains(@class, 'button')])

    pdriver.is_present("cn:test")

Examples
########

::

    if pdriver.is_visible("sv:login_btn'):
        pdriver.find("sv:login_btn").click()

    if pdriver.is_present("sv:hidden_field"):
        pdriver.find("sv:username_field").clear()

