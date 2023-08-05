Granting to unauthenticated
===========================

There are 3 special groups:

- Everybody, that everybody belongs to,

- Unauthenticated, that unauthenticated users belong to, and

- Authenticating, that authenticated users belong to.

Here's an example:

First, we'll set up a pluggable authentication utility containing a
principal folder, which we'll create first.



Create pluggable authentication utility and register it.

  >>> from zope.testbrowser.wsgi import Browser
  >>> manager_browser = Browser()
  >>> manager_browser.handleErrors = False
  >>> manager_browser.addHeader("Authorization", "Basic bWdyOm1ncnB3")
  >>> manager_browser.post("http://localhost/++etc++site/default/@@contents.html",
  ...   "type_name=BrowserAdd__zope.pluggableauth.authentication.PluggableAuthentication&new_value=PAU")


  >>> manager_browser.getLink("Registration").click()

Register PAU. First we get the registration page:

  >>> manager_browser.getControl("Register this object").click()

And then we can fill out and submit the form:

  >>> manager_browser.getControl("Register").click()

Add a Principal folder plugin to PAU. Again, we get the page, and then submit the form:

  >>> manager_browser.getLink("Principal Folder").click()
  >>> manager_browser.getControl(name="field.prefix").value = "users"
  >>> manager_browser.getControl(name="add_input_name").value = "users"
  >>> manager_browser.getControl("Add").click()

Next we'll view the contents page of the principal folder:

  >>> manager_browser.open("http://localhost/++etc++site/default/PAU/users/@@contents.html")
  >>> 'users' in manager_browser.contents
  True

And we'll add a principal, Bob:

  >>> manager_browser.getLink("Principal Information").click()
  >>> manager_browser.getControl(name="field.login").value = 'bob'
  >>> manager_browser.getControl(name="field.passwordManagerName").value = 'SHA1'
  >>> manager_browser.getControl(name="field.password").value = 'bob'
  >>> manager_browser.getControl(name="field.title").value = 'Bob Smith'
  >>> manager_browser.getControl(name="field.description").value = 'This is Bob'
  >>> manager_browser.getControl(name="add_input_name").value = 'bob'
  >>> manager_browser.getControl(name="UPDATE_SUBMIT").click()
  >>> manager_browser.open("http://localhost/++etc++site/default/PAU/users/@@contents.html")
  >>> u'bob' in manager_browser.contents
  True

Configure PAU, with registered principal folder plugin and
select any one credentials. Unfortunately, the option lists are computed dynamically in JavaScript, so
we can't fill the form out directly. Instead we must send a complete POST body. We're choosing
the users folder as the authenticator plugin, and the session utility as the credentials plugin.

  >>> manager_browser.open("http://localhost/++etc++site/default/PAU/@@configure.html")
  >>> manager_browser.post("http://localhost/++etc++site/default/PAU/@@configure.html",
  ...  r"""UPDATE_SUBMIT=Change&field.credentialsPlugins=U2Vzc2lvbiBDcmVkZW50aWFscw==&field.authenticatorPlugins=dXNlcnM="""
  ...  """&field.credentialsPlugins.to=U2Vzc2lvbiBDcmVkZW50aWFscw==&field.authenticatorPlugins.to=dXNlcnM=""")


Normally, the anonymous role has view, we'll deny it:

  >>> manager_browser.post("/++etc++site/AllRolePermissions.html",
  ...   """role_id=zope.Anonymous"""
  ...   """&Deny%3Alist=zope.View"""
  ...   """&Deny%3Alist=zope.app.dublincore.view"""
  ...   """&SUBMIT_ROLE=Save+Changes""")

Now, if we try to access the main page as an anonymous user,
we'll be unauthorized:


  >>> anon_browser = Browser()
  >>> anon_browser.open("http://localhost/")
  >>> print(anon_browser.url)
  http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F%40%40index.html

We'll even be unauthorized if we try to access it as bob:

  >>> bob_browser = Browser()
  >>> bob_browser.open("http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F")
  >>> bob_browser.getControl(name="login").value = 'bob'
  >>> bob_browser.getControl(name="password").value = 'bob'
  >>> bob_browser.getControl(name="SUBMIT").click()
  >>> print(bob_browser.url)
  http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F%40%40index.html


No, let's grant view to the authenticated group:

  >>> manager_browser.open("/@@grant.html")
  >>> 'principals.zcml' in manager_browser.contents
  True
  >>> manager_browser.getControl(name='field.principal.MQ__.search').click()

Once we've found him, we see what roles are available:

  >>> manager_browser.getControl(name="field.principal.MQ__.selection").displayValue = ['Authenticated Users']
  >>> manager_browser.getControl(name="field.principal.MQ__.apply").click()
  >>> 'zope.View' in manager_browser.contents
  True

  >>> manager_browser.post("/@@grant.html",
  ...   """field.principal=em9wZS5BdXRoZW50aWNhdGVk&field.principal.displayed=y"""
  ...   """&field.em9wZS5BdXRoZW50aWNhdGVk.permission.zope.View=allow"""
  ...   """&field.em9wZS5BdXRoZW50aWNhdGVk.permission.zope.app.dublincore.view=allow"""
  ...   """&GRANT_SUBMIT=Change""")

Now, with this, we can access the main page as bob, but not as an
anonymous user:

  >>> bob_browser.open("http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F")
  >>> bob_browser.getControl(name="login").value = 'bob'
  >>> bob_browser.getControl(name="password").value = 'bob'
  >>> bob_browser.getControl(name="SUBMIT").click()
  >>> print(bob_browser.url)
  http://localhost/


  >>> anon_browser.open("http://localhost/")
  >>> print(anon_browser.url)
  http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F%40%40index.html

###401 Unauthorized


Now, we'll grant to unauthenticated:

  >>> manager_browser.post("/@@grant.html",
  ...   """field.principal=em9wZS5Bbnlib2R5"""
  ...   """&field.em9wZS5Bbnlib2R5.permission.zope.View=allow"""
  ...   """&field.em9wZS5Bbnlib2R5.permission.zope.app.dublincore.view=allow"""
  ...   """&GRANT_SUBMIT=Change""")

With this, we can access the page as either bob or anonymous:

  >>> bob_browser.open("/")
  >>> print(bob_browser.url)
  http://localhost/

  >>> anon_browser.open("/")
  >>> print(anon_browser.url)
  http://localhost/


Now, we'll remove the authenticated group grant:

  >>> manager_browser.post("/@@grant.html",
  ...   """field.principal=em9wZS5BdXRoZW50aWNhdGVk"""
  ...   """&field.em9wZS5BdXRoZW50aWNhdGVk.permission.zope.View=unset"""
  ...   """&field.em9wZS5BdXRoZW50aWNhdGVk.permission.zope.app.dublincore.view=unset"""
  ...   """&GRANT_SUBMIT=Change""")

And anonymous people will be able to access the page, but bob won't be able to:

  >>> bob_browser.open("/")
  >>> print(bob_browser.url)
  http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F%40%40index.html

  >>> anon_browser.open("/")
  >>> print(anon_browser.url)
  http://localhost/


Now, we'll remove the unauthenticated group grant:

  >>> manager_browser.post("/@@grant.html",
  ...   """field.principal=em9wZS5Bbnlib2R5"""
  ...   """&field.em9wZS5Bbnlib2R5.permission.zope.View=unset"""
  ...   """&field.em9wZS5Bbnlib2R5.permission.zope.app.dublincore.view=unset"""
  ...   """&GRANT_SUBMIT=Change""")

  >>> bob_browser.open("/")
  >>> print(bob_browser.url)
  http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F%40%40index.html

  >>> anon_browser.open("/")
  >>> print(anon_browser.url)
  http://localhost/@@loginForm.html?camefrom=http%3A%2F%2Flocalhost%2F%40%40index.html


Finally, we'll grant to everybody:

  >>> manager_browser.post("/@@grant.html",
  ...   """field.principal=em9wZS5FdmVyeWJvZHk_"""
  ...   """&field.em9wZS5FdmVyeWJvZHk_.permission.zope.View=allow"""
  ...   """&field.em9wZS5FdmVyeWJvZHk_.permission.zope.app.dublincore.view=allow"""
  ...   """&GRANT_SUBMIT=Change""")

and both bob and anonymous can access:

  >>> bob_browser.open("/")
  >>> print(bob_browser.url)
  http://localhost/

  >>> anon_browser.open("/")
  >>> print(anon_browser.url)
  http://localhost/
