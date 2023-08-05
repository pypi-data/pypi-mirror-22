import re

try:
    from invoke.vendor.six import raise_from, iteritems
except ImportError:
    from six import raise_from, iteritems

from .config import Config, DataProxy
from .exceptions import Failure, AuthFailure, ResponseNotAccepted
from .runners import Local, Result
from .watchers import FailingResponder


class Context(DataProxy):
    """
    Context-aware API wrapper & state-passing object.

    `.Context` objects are created during command-line parsing (or, if desired,
    by hand) and used to share parser and configuration state with executed
    tasks (see :ref:`why-context`).

    Specifically, the class offers wrappers for core API calls (such as `.run`)
    which take into account CLI parser flags, configuration files, and/or
    changes made at runtime. It also acts as a proxy for its `~.Context.config`
    attribute - see that attribute's documentation for details.

    Instances of `.Context` may be shared between tasks when executing
    sub-tasks - either the same context the caller was given, or an altered
    copy thereof (or, theoretically, a brand new one).
    """
    def __init__(self, config=None):
        """
        :param config:
            `.Config` object to use as the base configuration.

            Defaults to an anonymous/default `.Config` instance.
        """

        #: The fully merged `.Config` object appropriate for this context.
        #:
        #: `.Config` settings (see their documentation for details) may be
        #: accessed like dictionary keys (``ctx.config['foo']``) or object
        #: attributes (``ctx.config.foo``).
        #:
        #: As a convenience shorthand, the `.Context` object proxies to its
        #: ``config`` attribute in the same way - e.g. ``ctx['foo']`` or
        #: ``ctx.foo`` returns the same value as ``ctx.config['foo']``.
        config = config if config is not None else Config()
        self._set(_config=config)

    @property
    def config(self):
        # Allows Context to expose a .config attribute even though DataProxy
        # otherwise considers it a config key.
        return self._config

    @config.setter
    def config(self, value):
        # NOTE: mostly used by client libraries needing to tweak a Context's
        # config at execution time; i.e. a Context subclass that bears its own
        # unique data may want to be stood up when parameterizing/expanding a
        # call list at start of a session, with the final config filled in at
        # runtime.
        self._set(_config=value)

    def run(self, command, **kwargs):
        """
        Execute a local shell command, honoring config options.

        Specifically, this method instantiates a `.Runner` subclass (according
        to the ``runner`` config option; default is `.Local`) and calls its
        ``.run`` method with ``command`` and ``kwargs``.

        See `.Runner.run` for details on ``command`` and the available keyword
        arguments.
        """
        runner_class = self.config.get('runner', Local)
        return runner_class(context=self).run(command, **kwargs)

    def sudo(self, command, **kwargs):
        """
        Execute a shell command, via ``sudo``.

        **Basics**

        In general, this method is identical to `run`, but adds a handful of
        convenient behaviors around invoking the ``sudo`` program. It doesn't
        do anything users could not do themselves by wrapping `run`, but the
        use case is too common to make users reinvent these wheels themselves.

        Specifically, `sudo`:

        * Places a `.FailingResponder` into the ``watchers`` kwarg (see
          :doc:`/concepts/watchers`) which:

            * searches for the configured ``sudo`` password prompt;
            * responds with the configured sudo password (``sudo.password``
              from the :doc:`configuration </concepts/configuration>`);
            * can tell when that response causes an authentication failure
              (e.g. if the system requires a password and one was not
              configured), and raises `.AuthFailure` if so.

        * Builds a ``sudo`` command string using the supplied ``command``
          argument, prefixed by various flags (see below);
        * Executes that command via a call to `run`, returning the result.

        **Flags used**

        ``sudo`` flags used under the hood include:

        - ``-S`` to allow auto-responding of password via stdin;
        - ``-p <prompt>`` to explicitly state the prompt to use, so we can be
          sure our auto-responder knows what to look for;
        - ``-u <user>`` if ``user`` is not ``None``, to execute the command as
          a user other than ``root``;
        - When ``-u`` is present, ``-H`` is also added, to ensure the
          subprocess has the requested user's ``$HOME`` set properly.

        **Configuring behavior**

        There are a couple of ways to change how this method behaves:

        - Because it wraps `run`, it honors all `run` config parameters and
          keyword arguments, in the same way that `run` does.

            - Thus, invocations such as ``c.sudo('command', echo=True)`` are
              possible, and if a config layer (such as a config file or env
              var) specifies that e.g. ``run.warn = True``, that too will take
              effect under `sudo`.

        - `sudo` has its own set of keyword arguments (see below) and they are
          also all controllable via the configuration system, under the
          ``sudo.*`` tree.

            - Thus you could, for example, pre-set a sudo user in a config
              file; such as an ``invoke.json`` containing ``{"sudo": {"user":
              "someuser"}}``.

        :param str password: Runtime override for ``sudo.password``.
        :param str user: Runtime override for ``sudo.user``.
        """
        prompt = self.config.sudo.prompt
        password = kwargs.pop('password', self.config.sudo.password)
        user = kwargs.pop('user', self.config.sudo.user)
        # TODO: allow subclassing for 'get the password' so users who REALLY
        # want lazy runtime prompting can have it easily implemented.
        # TODO: want to print a "cleaner" echo with just 'sudo <command>'; but
        # hard to do as-is, obtaining config data from outside a Runner one
        # holds is currently messy (could fix that), if instead we manually
        # inspect the config ourselves that duplicates logic. NOTE: once we
        # figure that out, there is an existing, would-fail-if-not-skipped test
        # for this behavior in test/context.py.
        # TODO: once that is done, though: how to handle "full debug" output
        # exactly (display of actual, real full sudo command w/ -S and -p), in
        # terms of API/config? Impl is easy, just go back to passing echo
        # through to 'run'...
        user_flags = ""
        if user is not None:
            user_flags = "-H -u {0} ".format(user)
        cmd_str = "sudo -S -p '{0}' {1}{2}".format(prompt, user_flags, command)
        watcher = FailingResponder(
            pattern=re.escape(prompt),
            response="{0}\n".format(password),
            sentinel="Sorry, try again.\n",
        )
        # Ensure we merge any user-specified watchers with our own.
        # NOTE: If there are config-driven watchers, we pull those up to the
        # kwarg level; that lets us merge cleanly without needing complex
        # config-driven "override vs merge" semantics.
        # TODO: if/when those semantics are implemented, use them instead.
        # NOTE: config value for watchers defaults to an empty list; and we
        # want to clone it to avoid actually mutating the config.
        watchers = kwargs.pop('watchers', list(self.config.run.watchers))
        watchers.append(watcher)
        try:
            return self.run(cmd_str, watchers=watchers, **kwargs)
        except Failure as failure:
            # Transmute failures driven by our FailingResponder, into auth
            # failures - the command never even ran.
            # TODO: wants to be a hook here for users that desire "override a
            # bad config value for sudo.password" manual input
            # NOTE: as noted in #294 comments, we MAY in future want to update
            # this so run() is given ability to raise AuthFailure on its own.
            # For now that has been judged unnecessary complexity.
            if isinstance(failure.reason, ResponseNotAccepted):
                # NOTE: not bothering with 'reason' here, it's pointless.
                # NOTE: using raise_from(..., None) to suppress Python 3's
                # "helpful" multi-exception output. It's confusing here.
                error = AuthFailure(result=failure.result, prompt=prompt)
                raise_from(error, None)
            # Reraise for any other error so it bubbles up normally.
            else:
                raise


class MockContext(Context):
    """
    A `.Context` whose methods' return values can be predetermined.

    Primarily useful for testing Invoke-using codebases.

    .. note::
        Methods not given `Results <.Result>` to yield will raise
        ``NotImplementedError`` if called (since the alternative is to call the
        real underlying method - typically undesirable when mocking.)
    """
    def __init__(self, config=None, **kwargs):
        """
        Create a ``Context``-like object whose methods yield `.Result` objects.

        :param config:
            A Configuration object to use. Identical in behavior to `.Context`.

        :param run:
            A data structure of `Results <.Result>`, to return from calls to
            the instantiated object's `~.Context.run` method (instead of
            actually executing the requested shell command).

            Specifically, this method accepts:

            - A single `.Result` object, which will be returned once.
            - An iterable of `Results <.Result>`, which will be returned on
              each subsequent call to ``.run``.
            - A map of command strings to either of the above, allowing
              specific call-and-response semantics instead of assuming a call
              order.

        :param sudo:
            Identical to ``run``, but whose values are yielded from calls to
            `~.Context.sudo`.

        :raises:
            ``TypeError``, if the values given to ``run`` or other kwargs
            aren't individual `.Result` objects or iterables.
        """
        # TODO: would be nice to allow regexen instead of exact string matches
        super(MockContext, self).__init__(config)
        for method, results in iteritems(kwargs):
            # Special convenience case: individual Result -> one-item list
            if (
                not hasattr(results, '__iter__')
                and not isinstance(results, Result)
                # No need for explicit dict test; they have __iter__
            ):
                err = "Not sure how to yield results from a {0!r}"
                raise TypeError(err.format(type(results)))
            self._set("_{0}".format(method), results)

    # TODO: _maybe_ make this more metaprogrammy/flexible (using __call__ etc)?
    # Pretty worried it'd cause more hard-to-debug issues than it's presently
    # worth. Maybe in situations where Context grows a _lot_ of methods (e.g.
    # in Fabric 2; though Fabric could do its own sub-subclass in that case...)

    def _yield_result(self, attname, command):
        # NOTE: originally had this with a bunch of explicit
        # NotImplementedErrors, but it doubled method size, and chance of
        # unexpected index/etc errors seems low here.
        try:
            value = getattr(self, attname)
            # TODO: thought there's a 'better' 2x3 DictType or w/e, but can't
            # find one offhand
            if isinstance(value, dict):
                if hasattr(value[command], '__iter__'):
                    result = value[command].pop(0)
                elif isinstance(value[command], Result):
                    result = value.pop(command)
            elif hasattr(value, '__iter__'):
                result = value.pop(0)
            elif isinstance(value, Result):
                result = value
                delattr(self, attname)
            return result
        except (AttributeError, IndexError, KeyError):
            raise_from(NotImplementedError, None)

    def run(self, command, *args, **kwargs):
        # TODO: perform more convenience stuff associating args/kwargs with the
        # result? E.g. filling in .command, etc? Possibly useful for debugging
        # if one hits unexpected-order problems with what they passed in to
        # __init__.
        return self._yield_result('_run', command)

    def sudo(self, command, *args, **kwargs):
        # TODO: this completely nukes the top-level behavior of sudo(), which
        # could be good or bad, depending. Most of the time I think it's good.
        # No need to supply dummy password config, etc.
        # TODO: see the TODO from run() re: injecting arg/kwarg values
        return self._yield_result('_sudo', command)
