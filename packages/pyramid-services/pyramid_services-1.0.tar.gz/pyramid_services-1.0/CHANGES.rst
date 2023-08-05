1.0 (2017-05-11)
================

Features
--------

- Allow the ``iface`` argument to be an arbitrary Python object / class.
  See https://github.com/mmerickel/pyramid_services/pull/10

Backward Incompatibilities
--------------------------

- Drop Python 2.6 and Python 3.3 support.

0.4 (2016-02-03)
================

Backward Incompatibilities
--------------------------

- Drop Python 3.2 support.

- Use the original service context interface as the cache key instead
  of the current context. This means the service will be properly created
  only once for any context satisfying the original interface.

  Previously, if you requested the same service from 2 different contexts
  in the same request you would receive 2 service objects, instead of
  a cached version of the original service, assuming the service was
  registered to satisfy both contexts.
  See https://github.com/mmerickel/pyramid_services/pull/12

0.3 (2015-12-13)
================

- When using ``request.find_service`` during or before traversal the
  ``request.context`` is not valid. In these situations the ``context``
  parameter will default to ``None`` instead of raising an exception.
  See https://github.com/mmerickel/pyramid_services/pull/8

- Add ``config.find_service_factory`` and ``request.find_service_factory``.
  See https://github.com/mmerickel/pyramid_services/pull/4

0.2 (2015-03-13)
================

- Change ``find_service(..., context=None)`` to use a context of ``None``.
  Previously this would fallback to using ``request.context`` if the
  ``context`` was ``None``. Now ``find_service`` will only fallback to
  ``request.context`` when no ``context`` argument is specified.
  See https://github.com/mmerickel/pyramid_services/pull/3

- Support ``introspectable`` for services so that they show up in the
  pyramid_debugtoolbar and elsewhere.
  See https://github.com/mmerickel/pyramid_services/pull/2

0.1.1 (2015-02-17)
==================

- Support for ``request.find_service``, ``config.register_service``, and
  ``config.register_service_factory``.
- Initial commits.
