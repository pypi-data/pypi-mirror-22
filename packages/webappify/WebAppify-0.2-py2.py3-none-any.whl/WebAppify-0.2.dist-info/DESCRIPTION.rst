WebAppify
=========

WebAppify is a simple module to easily create your own desktop apps of websites. WebAppify uses PyQt5 and QtWebKit or
QtWebEngine for displaying the web page, and works on Python 2.7 and Python 3.4 and up.

To create your own desktop web app, import and set up the WebApp class.

.. code:: python

   from webappify import WebApp

   app = WebApp('OpenStreetMap', 'https://www.openstreetmap.org', 'osm.png')
   app.run()

This will create a window with the website, using the icon provided.

Additional Options
------------------

Version 0.2 comes with the option of minimizing to the system tray. Simply pass ``canMinimizeToTray=True`` to the class
and a tray icon will be installed with the necessary menu options.

.. code:: python

   app = WebApp('OpenStreetMap', 'https://www.openstreetmap.org', 'osm.png', canMinimizeToTray=True)

Clicking on the tray icon will show the window, while right-clicking will show the menu.

.. note::

   If your site needs Flash Player, you'll need the appropriate Flash Player plugin installed system-wide. For QtWebKit
   you will need the NPAPI plugin, and for QtWebEngine you will need the PPAPI plugin.


