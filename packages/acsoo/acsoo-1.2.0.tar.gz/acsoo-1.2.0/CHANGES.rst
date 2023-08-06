Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

1.2.0 (unreleased)
------------------
- [IMP] add possibility to pass main config file as option
- [IMP] checklog: read default options from [checklog] section of config file
- [IMP] pylint: read default options from [pylint] section of config file
- [IMP] pylint: the module or package to lint may be provided with -m
- [IMP] flake8: read default options from [flake8] section of config file;
  the only option so far is ``config`` to provide an alternate flake8
  configuration file; this is useful so developer only need to type
  ``acsoo flake8`` locally, even when a specific configuration is needed,
  so it's trivial to run locally with the same config as in CI

1.1.0 (2017-05-25)
------------------
- [IMP] pylint: BREAKING the package to test must be provided explicitly,
  as soon as additional pylint options are provided,
  so as to enable easy local testing of a subset of a project. Examples:
  ``acsoo pylint -- -d some-message odoo``, ``acsoo pylint -- odoo.addons.xyz``
- [IMP] pylint: disable more code complexity errors: ``too-many-nested-blocks``,
  ``too-many-return-statements``
- [IMP] pylint: display messages causing failure last, so emails from CI
  that show the last lines of the log are more relevant
- [IMP] pylint: display summary of messages that did not cause failure, also
  when there is no failure
- [ADD] ``acsoo addons list`` and ``acsoo addons list-depends``
- [ADD] ``acsoo checklog``

1.0.1 (2017-05-21)
------------------
- First public release.
