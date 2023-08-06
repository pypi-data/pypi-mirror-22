
Bootstrap 4 files for miyadaiku static site generator
========================================================

Provides Bootstrap4 CSS and Javascript files.


Installation
-------------------

Use pip command to install Bootstrap 4. 

::

   $ pip install miyadaiku.themes.bootstrap4


`miyadaiku.themes.jquery` and `miyadaiku.themes.tether` are also installed automatically.


Configuraion
----------------------


In your config.yml file of your project, add following configuration at `themes` section.

::

   themes:
     - miyadaiku.themes.bootstrap4    # <---- add this line


Usage
----------------------

Add following code to your template files.

::

   <!-- include boolstrap4 -->
   {% include 'bootstrap4_css.html' %}

   <!-- include jquery.js -->
   {% include 'jquery.html' %}

   <!-- include tether.js -->
   {% include 'tether.html' %}

   <!-- include boolstrap4 js -->
   {% include 'bootstrap4_js.html' %}
