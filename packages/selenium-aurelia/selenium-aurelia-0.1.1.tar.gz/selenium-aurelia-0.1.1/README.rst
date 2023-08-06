Wrapper around selenium drivers to ease testing of `Aurelia <http://aurelia.io/>`__ based applications.

Inspired by `the aurelia plugin for protractor <https://github.com/aurelia/tools/blob/master/plugins/protractor.js>`__.


API
===

The ``AureliaDriver`` class takes one positionnal parameter: a selenium webdriver. The full list of drivers is available `here <http://selenium-python.readthedocs.io/api.htm>`__.

Options of AureliaDriver
------------------------

The ``AureliaDriver`` class takes the following keyword arguments:

- ``script_timeout`` (*default:*: 10): the timeout for `execute_async_script <http://selenium-python.readthedocs.io/api.html#selenium.webdriver.remote.webdriver.WebDriver.execute_async_script>`__. This is used internally to wait for the application to be loaded or to complete navigation.
- ``default_wait_time`` (*default:* 2): the time to wait by default in seconds. This is used by ``AureliaDriver.wait`` if no time is supplied and to wait for the in ``AureliaDriver.load_url`` to wait for Aurelia to complete the initialization of the page.
- ``wait_on_navigation`` wait for ``default_wait_time`` after each navigation before continuing the script.
- ``started_condition`` (*default:* None): it is possible that your app will be loaded before the AureliaDriver has the time to register the proper callback in the browser. In this case, ``load_url`` will fail because of a time out. To prevent this, you can specify a custom condition you know is fulfilled when Aurelia is started on your application. For instance, if your application has a spinner with the splash class, you can use: ``document.querySelector("[aurelia-app]").children[0].getAttribute('class') === 'splash'``.

load_url
--------

Load the given url and wait for Aurelia to be full initiazed.

- parameters:

  - ``url``: the url to open.

wait
----

Sleep for the specified amount of time. If no argument is provided or if seconds is lower or equal than 0, ``AureliaDriver.default_wait_time`` will be used.

- keyword arguments:

  - ``seconds`` (*default:* 0): number of seconds for which to sleep.

navigate
--------

Context manager in which you can to your navigation operation to ensure the app navigated to the new URL and was updated before continuing your tests. Use like this:

.. code:: python

    with driver.navigate():
        link.click()

    assert no_new_page

- keyword arguments:

  - ``wait`` (*default:* 0): time to wait after navigation before continuing. There are several cases to consider:
  
    #. If ``wait`` is greater than 0, the driver will wait for the specified time.
    #. If ``self.wait_on_navigation`` is ``True`` and ``wait`` is lower or equal than 0, the driver will wait for ``self.default_wait_time``.
    #. If ``self.wait_on_navigation`` is ``False`` and wait is lower or equal than 0, the driver will not wait.

find_element_by_binding
-----------------------

Return the first element matching the specified binding.

- parameters:

  - ``attr``: the name of the attribute used in the binding. For instance, in ``src.bind="heroSrc"`` it is ``src``.
  - ``value``: the value for which to look for. For instance, in ``src.bind="heroSrc"``, it is ``heroSrc``.

- keyword arguments:

  - bind_type (*default:* 'bind'): the type of binding to use. Possible values are: ``bind``, ``one-way``, ``two-way``.

find_elements_by_binding
------------------------

Return the list of all the elements matching the specified binding. See `find_element_by_binding` for details.


Full Example
============

You can have a look at the example script `in selenium_aurelia/test/example.py <https://framagit.org/Jenselme/selenium-aurelia/blob/master/selenium_aurelia/test/example.py>`__.


Issues
======

You can report issues on `the issues tracker <https://framagit.org/Jenselme/selenium-aurelia/issues>`__.


Changelog
=========

v0.1.1
------

- Add option to wait after navigation (``wait_on_navigation`` in constructor and ``wait`` in the ``navigate`` method).

v0.1.0
------

Initial release.

