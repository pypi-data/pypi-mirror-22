qmon - Redis Monitor
====================

|Join the chat at https://gitter.im/shubhamchaudhary/qmon|

|PyPI Version| |PyPI Monthly Downloads| |PyPI License| |GitHub tag|
|GitHub release|

|Build Status Travis-CI| |Coverage Status| |Circle CI| |Requirements
Status|

|GitHub issues| |Stories in Ready|

QMon is a redis queue monitor

Installation
============

.. code:: shell

    pip3 install qmon

Usage:
======

.. code:: shell

    > export HIP_TOKEN=MyHipChatToken
    > qmon --host localhost --port 6379 --queue-name a_key_in_redis --room RoomInHipChat
    [qmon.monitor] [2017-05-12 12:36:45,248] INFO : Connecting to hipchat
    [qmon.monitor] [2017-05-12 12:36:47,292] INFO : a_key_in_redis queue status: 6. Items: 6. Last Notify: 0
    [qmon.monitor] [2017-05-12 12:37:07,754] INFO : a_key_in_redis queue status: 11. Items: 11. Last Notify: 0
    [qmon.monitor] [2017-05-12 12:37:20,237] INFO : a_key_in_redis queue status: 16. Items: 16. Last Notify: 0
    [qmon.monitor] [2017-05-12 12:37:38,235] INFO : a_key_in_redis queue status: 10. Items: 10. Last Notify: 0

| This is how it'll appear in hipchat:
| |hipchat\_window|

Find us: \* `PyPi <https://pypi.python.org/pypi/qmon>`__

.. |Join the chat at https://gitter.im/shubhamchaudhary/qmon| image:: https://badges.gitter.im/shubhamchaudhary/qmon.svg
   :target: https://gitter.im/shubhamchaudhary/qmon?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |PyPI Version| image:: https://img.shields.io/pypi/v/qmon.svg
   :target: https://pypi.python.org/pypi/qmon
.. |PyPI Monthly Downloads| image:: https://img.shields.io/pypi/dm/qmon.svg
   :target: https://pypi.python.org/pypi/qmon
.. |PyPI License| image:: https://img.shields.io/pypi/l/qmon.svg
   :target: https://pypi.python.org/pypi/qmon
.. |GitHub tag| image:: https://img.shields.io/github/tag/shubhamchaudhary/qmon.svg
   :target: https://github.com/shubhamchaudhary/qmon/releases
.. |GitHub release| image:: https://img.shields.io/github/release/shubhamchaudhary/qmon.svg
   :target: https://github.com/shubhamchaudhary/qmon/releases/latest
.. |Build Status Travis-CI| image:: https://travis-ci.org/shubhamchaudhary/qmon.svg
   :target: https://travis-ci.org/shubhamchaudhary/qmon
.. |Coverage Status| image:: https://coveralls.io/repos/shubhamchaudhary/qmon/badge.svg?branch=master
   :target: https://coveralls.io/r/shubhamchaudhary/qmon?branch=master
.. |Circle CI| image:: https://circleci.com/gh/shubhamchaudhary/qmon.svg?style=svg
   :target: https://circleci.com/gh/shubhamchaudhary/qmon
.. |Requirements Status| image:: https://requires.io/github/shubhamchaudhary/qmon/requirements.svg?branch=master
   :target: https://requires.io/github/shubhamchaudhary/qmon/requirements/?branch=master
.. |GitHub issues| image:: https://img.shields.io/github/issues/shubhamchaudhary/qmon.svg?style=plastic
   :target: https://github.com/shubhamchaudhary/qmon/issues
.. |Stories in Ready| image:: https://badge.waffle.io/shubhamchaudhary/qmon.png?label=ready&title=Ready
   :target: https://waffle.io/shubhamchaudhary/qmon
.. |hipchat\_window| image:: http://i.imgur.com/G1vnPUm.png



