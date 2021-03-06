"""dRest core API connection library."""

from drest import interface, resource, request, serialization, meta, exc

class API(meta.MetaMixin):
    """
    Arguments:
    
        baseurl
            Translated to self._meta.baseurl (for convenience).
            
    Optional Arguments and Meta:
        
        baseurl
            The base url to the API endpoint.
            
        request
            The Request Handler class that handles requests
            
        resource
            The Resource handler class that handles resources.
            
        ignore_ssl_validation
            Whether or not to ignore ssl validation errors.  This option
            is passed down to the request handler.  Default: False.
            
    Usage
    
    .. code-block:: python
    
        import drest

        # Create a generic client api object
        api = drest.API('http://localhost:8000/api/v1/')
    
        # By default, auth() just appends its params to the URL so name the
        # parameters however you want them passed as.
        api.auth(api_user='john.doe', password='XXXXXXXXXXXX')
    
        # Make calls openly
        response, data = api.request('GET', '/users/1/')
    
        # Or attach a resource
        api.add_resource('users')
    
        # Get available resources
        api.resources
    
        # Get all objects of a resource
        response, objects = api.users.get()
    
        # Get a single resource with primary key '1'
        response, object = api.users.get(1)
    
        # Update a resource with primary key '1'
        response, data = api.users.get(1)
        updated_data = data.copy()
        updated_data['first_name'] = 'John'
        updated_data['last_name'] = 'Doe'
    
        response, object = api.users.update(data['id'], updated_data)
    
        # Create a resource
        user_data = dict(
                        username='john.doe',
                        password'oober-secure-password',
                        first_name='John',
                        last_name'Doe',
                        )
        response, data = api.users.create(user_data)
    
        # Delete a resource with primary key '1'
        response, data = api.users.delete(1)
    """
    class Meta:
        baseurl = None
        request = request.RequestHandler
        resource = resource.RESTResourceHandler
        ignore_ssl_validation = False
        
    def __init__(self, baseurl, **kw):
        kw['baseurl'] = baseurl
        super(API, self).__init__(**kw)        
        
        self._resources = []
        self._request = self._meta.request(**kw)
        request.validate(self._request)
        
    def auth(self, user, password, **kw):
        """
        This authentication mechanism implements HTTP Basic Authentication.
                        
        Required Arguments:
        
            user
                The API username.
                
            password
                The password of that user.
                
        """
        self._request.set_auth_credentials(user, password)
            
    def request(self, method, path, params={}):
        return self._request.request(method, path, params)
        
    @property
    def resources(self):
        return self._resources
        
    def add_resource(self, name, resource_handler=None, path=None):
        if not path:
            path = '%s' % name
        else:
            path = path.lstrip('/')
            
        if not resource_handler:
            handler = self._meta.resource
        else:
            handler = resource_handler
        
        
        handler = handler(baseurl=self._meta.baseurl, path=path, 
                          name=name, 
                          request=self._request
                          )
        resource.validate(handler)
        if hasattr(self, name):
            raise exc.dRestResourceError(
                "The object '%s' already exist on '%s'" % (name, self))
        setattr(self, name, handler)
        self._resources.append(name)
        
class TastyPieAPI(API):
    """
    This class implements an API client, specifically tailored for
    interfacing with `TastyPie <http://django-tastypie.readthedocs.org/en/latest>`_.
    
    Authentication Mechanisms
    
    Currently the only supported authentication mechanism are:
    
        * ApiKeyAuthentication
        * BasicAuthentication
    
    Usage
    
    Please note that the following example use ficticious resource data.  
    What is returned, and sent to the API is unique to the API itself.  Please
    do not copy and paste any of the following directly without modifying the
    request parameters per your use case.
    
    Create the client object, and authenticate with a user/api_key pair by 
    default:
    
    .. code-block:: python
    
        import drest
        api = drest.api.TastyPieAPI('http://localhost:8000/api/v0/')
        api.auth('john.doe', '34547a497326dde80bcaf8bcee43e3d1b5f24cc9')
    
    
    OR authenticate against HTTP Basic Auth:
    
    .. code-block:: python
    
        import drest
        api = drest.api.TastyPieAPI('http://localhost:8000/api/v0/',
                                    auth_mech='basic')
        api.auth('john.doe', 'my_password')
    
    
    As drest auto-detects TastyPie resources, you can view those at:
    
    .. code-block:: python    
    
        api.resources
        
    And access their schema:
    
    .. code-block:: python  
    
        api.users.schema
        
    As well as make the usual calls such as:
    
    .. code-block:: python  
    
        api.users.get()
        api.users.get(<pk>)
        api.users.put(<pk>, data_dict)
        api.users.post(data_dict)
        api.users.delete(<pk>)
        
    What about filtering? (these depend on how the `API is configured <http://django-tastypie.readthedocs.org/en/latest/resources.html#basic-filtering>`_):
    
    .. code-block:: python
    
        api.users.get(params=dict(username='admin'))
        api.users.get(params=dict(username__icontains='admin'))
        ...
        
    See :mod:`drest.api.API` for more standard usage examples.
        
    """
    class Meta:
        request = request.TastyPieRequestHandler
        resource = resource.TastyPieResourceHandler
        auto_detect_resources = True
        auth_mech = 'api_key'
        auth_mechanizms = ['api_key', 'basic']
        
    def __init__(self, *args, **kw):
        super(TastyPieAPI, self).__init__(*args, **kw)
        if self._meta.auto_detect_resources:
            self.find_resources()

    
    def auth(self, *args, **kw):
        """
        Authenticate the request, determined by Meta.auth_mech.  Arguments
        and Keyword arguments are just passed to the auth_mech function.
        
        """
        if self._meta.auth_mech in self._meta.auth_mechanizms:
            func = getattr(self, '_auth_via_%s' % self._meta.auth_mech)
            func(*args, **kw)
        else:
            raise exc.dRestAPIError("Unknown TastyPie auth mechanism.")
            
    def _auth_via_basic(self, user, password, **kw):
        """
        This is just a wrapper around drest.api.API.auth().
        
        """
        return super(TastyPieAPI, self).auth(user, password)
    
    def _auth_via_api_key(self, user, api_key, **kw):
        """
        This authentication mechanism adds an Authorization header for 
        user/api_key per the 
        `TastyPie Documentation <http://django-tastypie.readthedocs.org/en/latest/authentication_authorization.html>`_.
                        
        Required Arguments:
        
            user
                The API username.
                
            api_key
                The API Key of that user.
                
        """
        key = 'Authorization'
        value = 'ApiKey %s:%s' % (user, api_key)
        self._request.add_header(key, value)
       
    def find_resources(self):
        """
        Find available resources, and add them via add_resource().
        
        """
        response, data = self.request('GET', '/')
        for resource in list(data.keys()):
            if resource not in self._resources:
                self.add_resource(resource)
    