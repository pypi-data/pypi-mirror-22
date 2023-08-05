# Copyright (c) AppDynamics, Inc., and its affiliates
# 2015
# All Rights Reserved

"""API functions for custom reporting of BTs and exit calls.

"""

from __future__ import unicode_literals
from contextlib import contextmanager
import logging
import sys
import weakref

import appdynamics.agent
from appdynamics.lang import str
from appdynamics.agent.models.exitcalls import exit_point_type_name
from appdynamics.agent.models.frames import get_frame_info
from appdynamics.agent.models.transactions import ENTRY_CLI

__all__ = [
    'init',
    'shutdown',
    'start_bt',
    'end_bt',
    'get_active_bt_handle',
    'add_snapshot_data',
    'start_exit_call',
    'end_exit_call',
    'make_correlation_header',
    'exit_call',
    'bt',
    'CORRELATION_HEADER_NAME',
]

_agent = appdynamics.agent._agent
_bts = weakref.WeakValueDictionary()
_exit_calls = weakref.WeakValueDictionary()
_logger = logging.getLogger('appdynamics.agent.api')

NO_TIMEOUT = object()

# Name of the correlation header
CORRELATION_HEADER_NAME = appdynamics.agent.core.correlation.HEADER_NAME


def init(environ=None, timeout_ms=NO_TIMEOUT):
    """Start the AppDynamics Python Agent.

    You should call this at the very beginning of your instrumented app,
    preferably before doing any other imports, and before creating any other
    threads.

    Note that the agent initialization occurs asynchronously. This function
    returns immediately, but it's possible that the agent will not yet be
    ready to report business transactions. In this case, the ``start_bt``
    method will return ``None``.

    This function will never raise an exception.

    Optional Parameters
    -------------------
    environ : dict, optional
        If specified, a dictionary of environment variables to use to
        override the agent's configuration derived from the actual OS
        environment variables.

    timeout_ms : int or None, optional
        By default, this function returns immediately, even if the Python
        agent has not received its configuration from the controller.  If
        timeout_ms is ``None``, this function blocks until the agent is
        properly configured.  Otherwise, this function waits for up to
        timeout_ms for the agent to become ready.

    Returns
    -------
    bool
        True if the agent is properly configured when this function returns.

    """
    with _log_api_exception('init(environ=%r, timeout_ms=%r)', environ, timeout_ms):
        global _agent

        if _agent is None:
            _logger.info('Creating new AppDynamics Python Agent instance.')
            _agent = appdynamics.agent.bootstrap()

        if environ is not None:
            _logger.info('Updating agent config with provided environment dictionary.')
            _logger.debug('Incoming environ: %r' % environ)
            appdynamics.agent.configure(environ=environ)

        _logger.info('Starting AppDynamics Python Agent.')
        _agent.start()

        if timeout_ms is not NO_TIMEOUT:
            if timeout_ms:
                _logger.info('Waiting for up to %ds for agent to start up.' % timeout_ms)
            else:
                _logger.info('Waiting for agent to start up.')
            _agent.wait_for_start(timeout_ms=timeout_ms)

        return _agent.enabled

    return False


def shutdown(timeout_ms=None):
    """Shutdown the AppDynamics agent.

    This function ends all active BTs and waits for them to report.

    Optional Parameters
    -------------------

    timeout_ms: int, optional
        By default, this function waits until all pending BTs have been
        reported before returning.  If timeout_ms is set, this function
        will return after timeout_ms, regardless of whether all BTs have
        been reported.

    """
    with _log_api_exception('shutdown(timeout_ms=%r)' % timeout_ms):
        global _agent
        if _agent is not None:
            _agent.end_active_bts()
            _agent.wait_for_end(timeout_ms)
            _agent.stop()
            _agent = None


def start_bt(name, correlation_header=None):
    """Start a custom business transaction.

    There may be only one active BT per thread.  Attempts to start subsequent BTs
    in the same thread will return a ``bt_handle`` of ``None``.

    Consider using the ``bt`` context manager instead in cases where you start
    and end the BT in the same code (i.e., where you can wrap the whole BT in
    a ``with`` statement).

    Examples
    --------
    Given the code:

        setup()
        do_work()
        teardown()

    If you want to report `do_work` as a business transaction, you can either
    use ``start_bt`` and ``end_bt`` like so:

        from appdynamics.agent import api as appd
        setup()

        bt_handle = appd.start_bt('do work')
        try:
            do_work()
        except Exception as exc:
            raise
        finally:
            appd.end_bt(bt_handle, exc)

    Or you can use the ``bt`` context manager:

        setup()

        with bt('do work'):
            do_work()

        teardown()

    The latter is preferable, but only available when the BT starts and ends
    in the same context.

    Parameters
    ----------
    name : str
        The name to give the BT in the controller.

    Other Parameters
    ----------------
    correlation_header : str, optional
        If specified, a correlation header that has been generated by another
        AppDynamics agent and passed to this agent as a str.

    Returns
    -------
    BtHandle
        A handle that identifies this BT or, if no BT was started, None.

    See Also
    --------
    end_bt : End a BT.
    bt : A context manager that starts and ends a BT around your code. This is
         often easier than using ``start_bt`` and ``end_bt`` manually.

    """
    with _log_api_exception('start_bt(%r, correlation_header=%r)', name, correlation_header):
        bt = _agent.start_transaction(ENTRY_CLI, name, correlation_header=correlation_header)

        if bt is None:
            return None

        bt_handle = _get_bt_handle(bt)

        # Has this BT already been started?
        if bt_handle in _bts:
            return None

        _bts[bt_handle] = bt
        return bt_handle


def end_bt(bt_handle, exc=None):
    """End the BT identified by ``bt_handle``.

    See Also
    --------
    start_bt : Start a BT.

    """
    with _log_api_exception('end_bt(%r, exc=%r)', bt_handle, exc):
        bt = _bts.pop(bt_handle, None)

        if bt is None:
            return

        if exc:
            bt.add_exception(*sys.exc_info())

        _agent.end_transaction(bt)


def get_active_bt_handle(request):
    """Return the BT handle associated with this request object or None.

    `request` should be one of the following:

        Flask RequestContext
        Django HttpRequest
        CherryPy Request
        a WSGI environ dict

    """
    bt = _agent.get_current_bt()
    if bt is None:
        return None

    bt_handle = _get_bt_handle(bt)

    # This BT may not have originated from the API, so add it to _bts.
    _bts[bt_handle] = bt
    return bt_handle


def add_snapshot_data(bt_handle, key, value):
    """Add custom data that will be reported if this BT takes a snapshot.

    You can report custom data to help with diagnosing issues as part of a
    snapshot. The custom data are added to the BT but will only be reported if
    the BT contains a snapshot.

    Examples
    --------
    Start a BT and then add custom snapshot data:

        with appd.bt('login') as bt_handle:
            appd.add_snapshot_data(bt_handle, 'username', POST['username'])
            # ...

    Parameters
    ----------
    bt_handle : BtHandle
        A handle for a business transaction
    key : bytes, unicode
        The name of the data item to report in the snapshot. If the type is
        bytes, then the buffer must represent a UTF-8 encoded string.
    value
        The value to give the data. If it is bytes, then it is treated as a
        UTF-8 encoded string. If provided as unicode, it is directly reported.
        All other objects will have `str` called on them.

    """
    with _log_api_exception('add_custom_data(%r, %r, %r)', bt_handle, key, value):
        bt = _bts.get(bt_handle)
        if bt is None:
            return None

        bt.snapshot_user_data[key] = str(value)


def start_exit_call(bt_handle, exit_type, display_name, identifying_properties, operation=None,
                    optional_properties=None, exit_subtype=None):
    """Start a custom exit call within a business transaction.

    There may be only one active exit call per BT.  Attempts to start subsequent exit calls will
    return an exit_call_handle of `None`.

    Examples
    --------
    Given code that originally looks like this:

        try:
            db = custom_db.connect(host='financials-lb', port=3456)
            all_employees = db.query_path('/financials/employees')
            individual_contributors = all_employees.filter(lambda r: r.level < 3)
            salaries_by_dept = individual_contributors.sum(value='salary', group='dept', as='total')

            for dept, total in salaries_by_dept.extract('dept', 'total'):
                report_salary_data(dept, total)

    You can wrap it in a business transaction and report a custom exit call
    by changing the code to:

        from appdynamics.agent import api as appd
        appd.init()

        FINANCIALS_ID_PROPS = {'Host': 'financials-lb', 'Port': 3456, 'Vendor': 'CUSTOM DB'}

        with appd.bt('department rollup') as bt_handle:
            exit_call = appd.start_exit_call(bt_handle, appd.EXIT_DB, 'Financials Database', FINANCIALS_ID_PROPS)
            exc = None

            try:
                db = custom_db.connect(host='financials-lb', port=3456)
                all_employees = db.query_path('/financials/employees')
                individual_contributors = all_employees.filter(lambda r: r.level < 3)
                salaries_by_dept = individual_contributors.sum(value='salary', group='dept', as='total')

                for dept, total in salaries_by_dept.extract('dept', 'total'):
                    report_salary_data(dept, total)
            except Exception as exc:
                raise  # Assuming something above handles exceptions for you
            finally:
                end_exit_call(exit_call, exc)

    Alternatively, in cases like the above, you can use the ``exit_call``
    decorator to simplify the code:

        from appdynamics.agent import api as appd
        appd.init()

        FINANCIALS_ID_PROPS = {'Host': 'financials-lb', 'Port': 3456, 'Vendor': 'custom db'}

        with appd.bt('department rollup') as bt_handle:
            with appd.exit_call(bt_handle, appd.EXIT_DB, 'Financials Database', FINANCIALS_ID_PROPS):
                db = custom_db.connect(host='financials-lb', port=3456)
                all_employees = db.query_path('/financials/employees')
                individual_contributors = all_employees.filter(lambda r: r.level < 3)
                salaries_by_dept = individual_contributors.sum(value='salary', group='dept', as='total')

                for dept, total in salaries_by_dept.extract('dept', 'total'):
                    report_salary_data(dept, total)

    Parameters
    ----------
    bt_handle : BtHandle
        A handle for a business transaction
    exit_type : int
    display_name : str
        The first time an exit call with the given identifying properties is
        made, its display name in the controller will be set to whatever you
        pass here. This shows up in the UI as the label on the flow map.
    identifying_properties : dict
        Identifying properties are a set of name-value string pairs (a dict)
        that uniquely identify the downstream component. For example, for a
        database, the identifying properties might be the vendor of the
        database (e.g., "SQL Server"), the host name and port, and the
        name of the database. The key of the dict is the name of the
        property; the value is the value of the property.

    Other Parameters
    ----------------
    operation : str, optional
        A string describing the operation that is being performed, such as
        the URL of an HTTP request or a SQL query for a DB.
    optional_properties : dict, optional
        If specified, a dictionary of optional properties that will be shown
        in the controller UI for this exit call.
    exit_subtype : str, optional
        For CUSTOM exit point types, provide a subtype string to identify the
        backend type.

    Returns
    -------
    ExitCallHandle
        A handle that identifies this exit call, for passing to
        ``end_exit_call`` or ``make_correlation_header``.

    See Also
    --------
    end_exit_call : Must be called to end the exit call. If any exit calls
                    aren't ended when the BT is ended, then they are all
                    ended when the BT is ended.
    exit_call : A context manager that automatically calls ``start_exit_call``
                and ``end_exit_call`` around your code.

    """
    with _log_api_exception('start_exit_call(%r, %r, %r, %r, operation=%r, optional_properties=%r)', bt_handle,
                            exit_type, display_name, identifying_properties, operation, optional_properties):
        bt = _bts.get(bt_handle)
        if bt is None:
            return None

        if exit_subtype is None:
            exit_subtype = exit_point_type_name(exit_type)

        backend = _agent.backend_registry.get_api_backend(exit_type, exit_subtype, identifying_properties, display_name)
        backend.optional_properties.update(optional_properties or {})

        _logger.debug('Starting exit call.  %s, operation = %r.', backend, operation)
        exit_call = _agent.start_exit_call(bt, get_frame_info(1), backend, operation=operation)

        if exit_call is None:
            return None

        exit_call_handle = bt_handle, exit_call.sequence_info
        _exit_calls[exit_call_handle] = exit_call
        return exit_call_handle


def end_exit_call(exit_call_handle, exc=None):
    """End the exit call identified by ``exit_call_handle``.

    See Also
    --------
    start_exit_call : Start an exit call.

    """
    with _log_api_exception('end_exit_call(%r, exc=%r)', exit_call_handle, exc):
        exit_call = _exit_calls.pop(exit_call_handle, None)
        if exit_call is None:
            return

        bt = _bts.get(exit_call_handle[0])
        if bt is None:
            return

        _agent.end_exit_call(bt, exit_call, get_frame_info(1), exc_info=exc and sys.exc_info())


def make_correlation_header(bt_handle, exit_call_handle, do_not_resolve=False):
    """Make a correlation header for a custom exit call.

    If you are performing custom exit calls to other instrumented tiers, adding
    a correlation header allows continuing BTs on the downstream tier.  It is
    up to you to send the header, as well as parse it at the other end and
    pass it to ``start_bt``.

    The work flow will be:

        with api.bt('important work') as bt:
            with api.exit_call(bt, api.EXIT_HTTP, ...) as exit_call:
                correlation_header = api.make_correlation_header(bt, exit_call)
                payload.headers.update(dict(correlation_header))
                payload.send()

    And, on the downstream tier one could parse the header and use it in the continuing bt:

        correlation_header = upstream_payload.headers[api.CORRELATION_HEADER_NAME]
        with apt.bt('downstream_work', correlation_header):
            some_work()

    Parameters
    ----------
    bt_handle : BtHandle
        A handle identifying a business transaction.
    exit_call_handle : ExitCallHandle
        A handle identifying an exit call.

    Returns
    -------
    Correlation header tuple (name of the header, header itself):
    A tuple (appdynamics.agent.api.CORRELATION_HEADER_NAME, header)

    """
    with _log_api_exception('make_correlation_header(%r, %r, do_not_resolve=%r)', bt_handle, exit_call_handle,
                            do_not_resolve):
        bt = _bts.get(bt_handle)
        exit_call = _exit_calls.get(exit_call_handle)
        return appdynamics.agent.core.correlation.make_header(_agent, bt, exit_call, do_not_resolve=do_not_resolve)


@contextmanager
def bt(*args, **kwargs):
    """Context manager for reporting some work as a business transaction.

    Yields
    ------
    BtHandle
        A handle for passing this BT to other functions, such as to `start_exit_call`.


    Examples
    --------

    If you have some code that looks like this:

        do_some_work()
        more_work()
        something_else()

    To report this section of code as a business transaction, modify it to
    read:

        with appdynamics.agent.api.bt('important work'):
            do_some_work()
            more_work()
            something_else()

    With this change, you can then look in the AppDynamics controller to see
    how often this section of code is hit, how long it takes for this code to
    run (down to the timing for individual lines of code), supported exit
    calls made from within this section of code (e.g., calls to MySQL,
    PostgreSQL, Redis, Memcached, HTTP clients, etc.), any uncaught
    exceptions raised by this code, and more.

    This function takes the same argument as `start_bt`.

    See Also
    --------
    start_bt : If you need to start and end the BT in different places in your
               code, you can explicitly use ``start_bt`` and ``end_bt``.

    """
    exc = None
    bt_handle = None
    try:
        bt_handle = start_bt(*args, **kwargs)
        yield bt_handle
    except Exception as e:
        exc = e
        raise
    finally:
        if bt_handle:
            end_bt(bt_handle, exc)


@contextmanager
def exit_call(*args, **kwargs):
    """Context manager for adding exit calls to a business transaction.

    Yields
    ------
    ExitCallHandle
        An handle for passing this exit call to other functions, such as to
        ``make_correlation_header``.

    Examples
    --------
    If you have code which looks like this:

        data = do_some_work()
        cache.set(data)

    You can report a business transaction with a custom exit call by modifying it to:

        with api.bt('important work') as bt:
            data = do_some_work()

            cache_props = {'Vendor': 'APPDYNAMICS', 'Server Pool': '10.1.1.1'}
            with api.exit_call(bt, api.EXIT_CACHE, 'custom cache', cache_props, operation='SET') as exit_call:
                correlation_header = api.make_correlation_header(bt, exit_call)
                data.add(correlation_header)
                cache.set(data)

    This function takes the same arguments as ``start_exit_call``.

    See Also
    --------
    start_exit_call: If you need to start and end exit calls in different
                     places in your code, you can use ``start_exit_call``
                     and ``end_exit_call``.

    """
    exc = None
    exit_call_handle = None
    try:
        exit_call_handle = start_exit_call(*args, **kwargs)
        yield exit_call_handle
    except Exception as e:
        exc = e
        raise
    finally:
        if exit_call_handle:
            end_exit_call(exit_call_handle, exc)


def _get_bt_handle(bt):
    return bt.request_id


@contextmanager
def _log_api_exception(*args):
    try:
        yield
    except:
        if _agent:
            _logger.exception(*args)
