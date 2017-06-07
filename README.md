repository.xbmc.chakra
======================

This KODI repository currently contains the following addons, 
 * plugin.video.chakra.dn : addon for watching daily news from Democracy Now!

Installation
============

 1. Simply download the [repository zip](https://github.com/chakravyu/repository.xbmc.chakra/blob/master/repository.xbmc.chakra/repository.xbmc.chakra-1.2.0.zip) and install it in XBMC.
 2. Read the following [guide](http://wiki.xbmc.org/index.php?title=HOW-TO:Install_an_Add-on_from_a_zip_file) on the XBMC wiki to learn how to install addons from a repository.


Acknowledgements
================

To, 
 * [xbmcswift](https://github.com/jbeluch/xbmcswift2) project : for making it ridiculously easy to write xbmc addons.
 * [KODI](https://kodi.tv/) : for bringing the online world to our television sets.

Developer Notes
===============
When installing the xbmcswift environment as described at http://xbmcswift2.readthedocs.io/en/latest/installation.html,
 * the virtualenv wrapper installation is done by 'sudo pip install virtualenvwrapper'
 * before building the virtual environment, you need to source the virtualenvwrapper.sh (usually found at /usr/local/bin/virtualenvwrapper.sh)

To deploy a new version,
 * update the version in the plugin addon.xml file
 * update the version in the repository addon.xml file
 * generate new version : run 'python ./repo_prep.py' from the root directory.

License
=======

Copyright © 2014 - 2016 Cherian Mathew / Sunayana Ghosh

[![Creative Commons License](http://i.creativecommons.org/l/by-nc/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc/4.0/deed.en_US)
This work is licensed under a [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/deed.en_US)

Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied.
See the License for the specific language governing rights and limitations under the License.


Attribution
===========

For crediting this work, please use the following attribution,

[repository.xbmc.chakra](https://github.com/chakravyu/repository.xbmc.chakra) by [chakravyu](https://github.com/chakravyu) is licensed under [Creative Commons Attribution-NonCommercial 4.0 International License](http://creativecommons.org/licenses/by-nc/4.0/deed.en_US)


Disclaimer
==========
This software makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties, including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights. Further, this software does not warrant or make any representations concerning the accuracy, likely results, or reliability of the use of the materials on the internet web site where from data is retrieved or otherwise relating to such materials or on any sites linked to this addon. Videos are sourced from video-hosting websites that are having full rights to remove such access to video if required.
