=======================================================
ZConfig logging support for raven
=======================================================

This package allows enabling `raven
<https://docs.sentry.io/clients/python/>`_, the Python interfacet to
`Sentry <https://sentry.io>`_ via a `ZConfig logging configuration <http://zconfig.readthedocs.io/en/latest/using-logging.html>`_
like::

  <logger>
    %import j1m.ravenzconfig
    <sentry>
      dsn https://abc:def@example.com/42
    </sentry>
  </logger>

Additional options are supported, including logging level and options
accepted by the raven client.  See the `raven client documentation
<https://docs.sentry.io/clients/python/advanced/>`_.

Here's an example that uses all of the options::

  <logger>
     %import j1m.ravenzconfig
     <sentry>
       level WARNING
       dsn https://abc:def@example.com/42
       site test-site
       name test
       release 42.0
       environment testing
       exclude_paths /a /b
       include_paths /c /d
       sample_rate 0.5
       list_max_length 9
       string_max_length 99
       auto_log_stacks true
       processors x y z
     </sentry>
   </logger>

The defaults for level and sample_rate are ERROR and 1.0. For other
options, other than the required ``dsn``, the defaults are unset.
