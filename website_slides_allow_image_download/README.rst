.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===================================================
Website Slides: Keep Original Image for Downloading
===================================================

* By default Odoo resizes the images that get uploaded to channels to 
  a max size of 1920x1920. This can be problematic if you want to e.g.
  share originals of high resolution marketing materials.
* This module adds a configurable option to keep also the original image 
  when uploading, and adds a Download button to frontend, where the 
  visitor can access the original.

Configuration
=============
* Enable the "Store also Uncompressed Versions of Images" and 
  "Show Download Link for Images" settings in eLearning configuration

Usage
=====
* Create a slide with a high resolution image either
  - Via frontend's "Upload new content", you can use the type "Presentation"
  - Via backend, you can use the type "Document"
* Go to the slide page in frontend, and you will see a Download button
* For any legacy images that may exist from before the module was 
  installed, the button downloads the compressed image provided by Odoo core.
* Note: if you want to change the image of an existing slide via backend, 
  change the slide type briefly back to Documentation, so that the Content
  field shows up and you can re-upload the image.
  

Known issues / Roadmap
======================
\-

Credits
=======

Contributors
------------

* Valtteri Lattu <valtteri.lattu@tawasta.fi>
* Timo Talvitie <timo.talvitie@tawasta.fi>

Maintainer
----------

.. image:: https://tawasta.fi/templates/tawastrap/images/logo.png
   :alt: Oy Tawasta OS Technologies Ltd.
   :target: https://tawasta.fi/

This module is maintained by Oy Tawasta OS Technologies Ltd.
