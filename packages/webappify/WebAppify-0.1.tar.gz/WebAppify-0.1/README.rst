WebAppify
=========

WebAppify is a simple module to easily create your own desktop apps of websites.

To create your own desktop web app, import and set up the WebApp class.

.. code:: python

   from webappify import WebApp

   app = WebApp('OpenStreetMap', 'https://www.openstreetmap.org', 'osm.png')
   app.run()

This will create a window with the website, using the icon provided.
