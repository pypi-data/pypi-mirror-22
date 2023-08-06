By [TCell](https://www.tcell.io/).

TCell Hooks is to be used in conjuction with the [tcell_agent](https://pypi.python.org/pypi/tcell_agent) to allow for custom event notifications of login failures and login successes.

## Getting started

You can add it to your requirements.txt file with:

```python
tcell_hooks==1.0.0
```

Then run `pip install -r requirements.txt`

There are two options for calling the hooks from your application code:

By providing a Django/Flask request object and having the TCell Agent extract the relevant details from it:

```python
from tcell_hooks.v1 import send_django_login_event, LOGIN_SUCCESS

send_django_login_event(
  status=LOGIN_SUCCESS,
  django_request=request,
  user_id="tcell@tcell.io",
  session_id="124KDJFL3234"
)
```

```python
from tcell_hooks.v1 import send_flask_login_event, LOGIN_SUCCESS

send_flask_login_event(
  status=LOGIN_SUCCESS,
  flask_request=request,
  user_id="tcell@tcell.io",
  session_id="124KDJFL3234"
)
```

Or by providing each individual piece of information required for the TCell event:

```python
from tcell_hooks.v1 import send_login_event, LOGIN_SUCCESS

send_login_event(
  status=LOGIN_SUCCESS,
  session_id="124KDJFL3234",
  user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) ...",
  referrer="http://192.168.99.100:3000/",
  remote_address="192.168.99.1",
  header_keys=["HOST", "USER_AGENT", "ACCEPT", "REFERER", "ACCEPT_ENCODING", "ACCEPT_LANGUAGE", "COOKIE"],
  user_id="tcell@tcell.io",
  document_uri="/users/auth/doorkeeper/callbackuri"
)
```

The available statuses are:

`LOGIN_SUCCESS`

`LOGIN_FAILURE`


## Important Note

If the [tcell_agent](https://pypi.python.org/pypi/tcell_agent) is not installed or if it's disabled, this code will do nothing and should have no performance effect on your app.
