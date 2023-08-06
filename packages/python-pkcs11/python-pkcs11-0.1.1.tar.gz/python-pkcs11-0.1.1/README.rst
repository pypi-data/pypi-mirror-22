Python PKCS#11 - High Level Wrapper API
=======================================

A high level, "more Pythonic" interface to the PKCS#11 (Cryptoki) standard
to support HSM and Smartcard devices in Python.

The interface is designed to follow the logical structure of a HSM, with
useful defaults for obscurely documented parameters. Many APIs will optionally
accept iterables and act as generators, allowing you to stream large data
blocks in a straightforward way.

Source: https://github.com/danni/python-pkcs11

Documentation: http://python-pkcs11.readthedocs.io/en/latest/

Getting Started
---------------

Install from Pip:

::

    pip install python-pkcs11


Or build from source:

::

    python setup.py build

Assuming your PKCS#11 library is set as `PKCS_MODULE` and contains a
token named `DEMO`:

AES
~~~

::

    import pkcs11

    # Initialise our PKCS#11 library
    lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
    token = lib.get_token(token_label='DEMO')

    data = b'INPUT DATA'

    # Open a session on our token
    with token.open(user_pin='1234') as session:
        # Generate an AES key in this session
        key = session.generate_key(pkcs11.KeyType.AES, 256, store=False)

        # Get an initialisation vector
        iv = session.generate_random(128)  # AES blocks are fixed at 128 bits
        # Encrypt our data
        crypttext = key.encrypt(data, mechanism_param=iv)

RSA
~~~

::

    import pkcs11

    lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
    token = lib.get_token(token_label='DEMO')

    data = b'INPUT DATA'

    # Open a session on our token
    with token.open(user_pin='1234') as session:
        # Generate an RSA keypair in this session
        pub, priv = session.generate_keypair(pkcs11.KeyType.RSA, 2048, store=False)

        # Encrypt as one block
        crypttext = pub.encrypt(data)


Diffie-Hellman
~~~~~~~~~~~~~~

::

    import pkcs11

    lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
    token = lib.get_token(token_label='DEMO')

    with token.open() as session:
        # Given shared Diffie-Hellman parameters
        parameters = session.create_domain_parameters(KeyType.DH, {
            Attribute.PRIME: prime,  # Diffie-Hellman parameters
            Attribute.BASE: base,
        })

        # Generate a DH key pair from the public parameters
        public, private = parameters.generate_keypair()

        # Share the public half of it with our other party.
        _network_.write(public[Attribute.VALUE])
        # And get their shared value
        other_value = _network_.read()

        # Derive a shared session key with perfect forward secrecy
        session_key = private.derive_key(
            KeyType.AES, 128,
            mechanism_param=other_value)


Elliptic-Curve Diffie-Hellman
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    import pkcs11

    lib = pkcs11.lib(os.environ['PKCS11_MODULE'])
    token = lib.get_token(token_label='DEMO')

    with token.open() as session:
        # Given DER encocded EC parameters, e.g. from
        #    openssl ecparam -outform der -name <named curve>
        parameters = session.create_domain_parameters(KeyType.EC, {
            Attribute.EC_PARAMS: ecparams,
        })

        # Generate a DH key pair from the public parameters
        public, private = parameters.generate_keypair()

        # Share the public half of it with our other party.
        _network_.write(public[Attribute.EC_POINT])
        # And get their shared value
        other_value = _network_.read()

        # Derive a shared session key
        session_key = private.derive_key(
            KeyType.AES, 128,
            mechanism_param=(KDF.NULL, None, other_value))

Tested Compatibility
--------------------

Things that should almost certainly work.

Python version:

* 3.4 (with `aenum`)
* 3.5 (with `aenum`)
* 3.6

PKCS#11 version:

* 2.4

Devices/Libraries:

* SoftHSMv2
* Thales nCipher (Security World)

Mechanisms:

* AES
* RSA
* Diffie-Hellman
* ECDH

Operations:

* Encrypt, Decrypt
* Sign, Verify
* Wrap, Unwrap
* Generate Key
* Generate Keypair
* Derive Key
* Generate Random
* Create, Copy and Destroy objects (if supported by backend)

Feel free to send pull requests for any functionality that's not exposed. The
code is designed to be readable and expose the PKCS#11 spec in a
straight-forward way.

If you want your device supported, get in touch!

More info on PKCS#11
--------------------

The latest version of the PKCS#11 spec is available from OASIS:

http://docs.oasis-open.org/pkcs11/pkcs11-base/v2.40/pkcs11-base-v2.40.html

You should also consult the documentation for your PKCS#11 implementation.
Many implementations expose additional vendor options configurable in your
environment, including alternative features, modes and debugging
information.

License
-------

MIT License

Copyright (c) 2017 Danielle Madeley

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
