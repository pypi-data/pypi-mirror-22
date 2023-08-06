# atlassian-jwt (Python)

[![codebeat badge](https://codebeat.co/badges/aea3b0ad-32b1-403e-a8e9-543ecd7dd778)](https://codebeat.co/projects/bitbucket-org-atlassian-atlassian-jwt-py/ratings)

[JSON Web Token](https://jwt.io/) (JWT) authentication and encoding library for Python 2 and 3.
Extends [pyjwt](https://github.com/jpadilla/pyjwt) to include Atlassian Connect's custom
[query string hash](https://developer.atlassian.com/blog/2015/01/understanding-jwt/) (qsh) claim.

This package is on [pypi](https://pypi.python.org/pypi/atlassian-jwt) so you can use pip to install
it

    pip install atlassian-jwt


## Tenant information

This package makes references to Atlassian Connect's
[tenant information data structure](https://developer.atlassian.com/static/connect/docs/latest/modules/lifecycle.html).
Specfically the `clientKey` and `sharedSecret` fields are used when encoding a JWT token. Here is an
example of the complete tenant information data structure as is passed to a Connect Addon with the
`installed` lifecycle callback.

    {
      "key": "installed-addon-key",
      "clientKey": "unique-client-identifier",
      "publicKey": "MIGf....ZRWzwIDAQAB",
      "sharedSecret": "a-secret-key-not-to-be-lost",
      "serverVersion": "server-version",
      "pluginsVersion": "version-of-connect",
      "baseUrl": "http://example.atlassian.net",
      "productType": "jira",
      "description": "Atlassian JIRA at https://example.atlassian.net",
      "serviceEntitlementNumber": "SEN-number",
      "eventType": "installed"
    }

Where

* *clientKey* is an identifying key for the Atlassian product instance that the add-on was installed
  into.
* *sharedSecret* is the string that should be used to sign outgoing JWT tokens and validate incoming
  JWT tokens.


## Authentication

This package provides an abstract base class that can be subclassed to provide authentication to an
Atlassian Connect Addon. Here is an example of that use

    import atlassian_jwt

    class MyAddon(atlassian_jwt.Authenticator):
        def __init__(self, tenant_info_store):
            super(MyAddon, self).__init__()
            self.tenant_info_store = tenant_info_store

        def get_shared_secret(self, client_key):
            tenant_info = self.tenant_info_store.get(client_key)
            return tenant_info['sharedSecret']

    my_auth = MyAddon(tenant_info_store)
    try:
        client_key = my_auth.authenticate(http_method, url, headers)
        # authentication succeeded
    except atlassian_jwt.DecodeError:
        # authentication failed
        pass


## Encoding

Atlassian Connect Addon can make API calls back to the host application. These API calls include a
JWT token for authentication. This package provides an `encode_token` function to do this work. Here
is an example of its use

    import atlassian_jwt

    token = atlassian_jwt.encode_token(http_method, url, **tenant_info)
    headers = {'Authorization': 'JWT {}'.format(token)}


## Understanding JWT for Atlassian Connect

* [Understanding JWT for Atlassian Connect](https://developer.atlassian.com/blog/2015/01/understanding-jwt/)
* [Understanding JWT](https://developer.atlassian.com/static/connect/docs/latest/concepts/understanding-jwt.html)
* [Creating a query string hash](https://developer.atlassian.com/static/connect/docs/latest/concepts/understanding-jwt.html#qsh)


## Running the tests

    pip2.7 install -e . && pip2.7 install -r requirements.txt && python2.7 -m pytest
    pip3.5 install -e . && pip3.5 install -r requirements.txt && python3.5 -m pytest