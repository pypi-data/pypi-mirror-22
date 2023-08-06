====================
Misago 0.5 Redirects
====================

This Misago app provides redirects for forums that were migrated from Misago 0.5 to Misago 0.6 and onwards.

This application exists because Misago 0.7 deprecates and removes the `misago.datamover` module that originally handled the redirects from old urls to new ones as part of larger package of migrating data from Misago 0.5.


Installation
============

To install package, run following command when you are in virtualenv that you've used to install Misago:

    pip install misago-05-redirects

This will install the redirects app in your envinroment and let you enable it in your site configuration. To do this, edit your `settings.py`, find `INSTALLED_APPS` in it, and append following line to it:

    'misago05redirects',


Next, open your `urls.py` and find line below:

    url(r'^', include('misago.urls', namespace='misago')),

Now, prepend new line before it so it looks like this:

    url(r'^', include('misago05redirects.urls')),
    url(r'^', include('misago.urls', namespace='misago')),

It's important for new line to come before Misago's one, or Misago's url's handler will intercept and fail on calls to some urls like user lists.

This is it.


Authors
=======

**Rafał Pitoń**

* http://rpiton.com
* http://github.com/rafalp
* https://twitter.com/RafalPiton


Copyright and license
=====================

Copyright © 2017 `Rafał Pitoń <http://github.com/ralfp>`_
This program comes with ABSOLUTELY NO WARRANTY.

This is free software and you are welcome to modify and redistribute it under the conditions described in the license.
For the complete license, refer to LICENSE.rst
