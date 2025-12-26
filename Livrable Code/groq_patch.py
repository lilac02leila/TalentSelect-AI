"""
Patch module to fix groq proxies error.
This must be imported BEFORE any langchain_groq imports.
"""
import os

# Remove proxy environment variables
proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
for var in proxy_vars:
    os.environ.pop(var, None)

# Patch groq.Client to ignore proxies parameter
try:
    import groq
    
    # Store original __init__
    _original_client_init = groq.Client.__init__
    
    def _patched_client_init(self, *args, **kwargs):
        """Patched __init__ that removes proxies parameter."""
        # Remove proxies if present
        kwargs.pop('proxies', None)
        # Call original __init__
        return _original_client_init(self, *args, **kwargs)
    
    # Apply patch
    groq.Client.__init__ = _patched_client_init
    
except (ImportError, AttributeError):
    pass

# Function to patch langchain_groq - call this after importing langchain_groq
def patch_langchain_groq():
    """Patch langchain_groq.ChatGroq to remove proxies parameter."""
    try:
        import langchain_groq
        if hasattr(langchain_groq, 'ChatGroq'):
            _original_chatgroq_init = langchain_groq.ChatGroq.__init__
            
            def _patched_chatgroq_init(self, *args, **kwargs):
                """Patched ChatGroq.__init__ that removes proxies parameter."""
                # Remove proxies if present
                kwargs.pop('proxies', None)
                
                # Also patch the client creation if it happens inside
                # Check if there's a _client attribute being set
                try:
                    result = _original_chatgroq_init(self, *args, **kwargs)
                    # After initialization, check if client was created with proxies
                    if hasattr(self, '_client') and self._client is not None:
                        # Client already created, should be fine
                        pass
                    return result
                except TypeError as e:
                    if 'proxies' in str(e):
                        # If error mentions proxies, try again without it
                        kwargs.pop('proxies', None)
                        return _original_chatgroq_init(self, *args, **kwargs)
                    raise
            
            langchain_groq.ChatGroq.__init__ = _patched_chatgroq_init
            
            # Also patch the _default_client method if it exists
            if hasattr(langchain_groq.ChatGroq, '_default_client'):
                _original_default_client = langchain_groq.ChatGroq._default_client
                
                def _patched_default_client(*args, **kwargs):
                    kwargs.pop('proxies', None)
                    return _original_default_client(*args, **kwargs)
                
                langchain_groq.ChatGroq._default_client = _patched_default_client
            
            return True
    except (ImportError, AttributeError) as e:
        pass
    return False

# Try to patch if langchain_groq is already imported
patch_langchain_groq()

