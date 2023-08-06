The `Python keyring lib <https://github.com/jaraco/keyring>`_ is a
cross-platform interface to store and retrieve passwords and other secret
information.

This is a keyring backend for Linux that only needs pure Python dependencies.
Like the main *SecretService* backend, it uses DBus to talk to the secret
service daemon. However, the *SecretService* backend relies on system libraries,
which makes installation more difficult. This backend uses `Jeepney
<https://pypi.python.org/pypi/jeepney>`_, a pure Python DBus backend.

To use this module, simply install it and use the ``keyring`` API as normal; if
the main *SecretService* backend is not available, keyring should
automatically detect and use ``keyring_jeepney``.

To explicitly use this module::

    import keyring
    import keyring_jeepney
    keyring.set_keyring(keyring_jeepney.Keyring())

The standard SecretService backend has been much better tested than this one,
so you probably want to use that one where practical.
