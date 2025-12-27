"""
Patch module to fix groq proxies error.
This must be imported BEFORE any langchain_groq imports.
"""
import os
import functools
import sys

# Remove proxy environment variables
proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'ALL_PROXY', 'all_proxy']
for var in proxy_vars:
    os.environ.pop(var, None)

# Global variable to track if groq.Client is patched
_groq_client_patched = False
_original_client_init_stored = None
_original_client_class = None

# Patch groq.Client to ignore proxies parameter
# This must be done BEFORE langchain_groq imports groq
def _patch_groq_client():
    """Patch groq.Client to remove proxies parameter."""
    global _groq_client_patched, _original_client_init_stored, _original_client_class
    
    if _groq_client_patched:
        return True
    
    try:
        # Import groq if available
        if 'groq' not in sys.modules:
            import groq
        else:
            groq = sys.modules['groq']
        
        # Store original __init__ if it exists and not already patched
        if hasattr(groq, 'Client') and hasattr(groq.Client, '__init__'):
            # Check if already patched
            if hasattr(groq.Client.__init__, '_groq_patch_applied'):
                _groq_client_patched = True
                return True
            
            # Store the original class and __init__ before patching
            _original_client_class = groq.Client
            _original_client_init_stored = groq.Client.__init__
            
            # Also store __new__ if it exists
            _original_client_new_stored = None
            if hasattr(groq.Client, '__new__'):
                _original_client_new_stored = groq.Client.__new__
            
            def _clean_proxy_kwargs(kwargs):
                """Helper function to remove all proxy-related parameters."""
                kwargs.pop('proxies', None)
                kwargs.pop('proxy', None)
                kwargs.pop('http_proxy', None)
                kwargs.pop('https_proxy', None)
                
                # Also remove any nested proxy settings
                if 'http_client' in kwargs:
                    if isinstance(kwargs['http_client'], dict):
                        kwargs['http_client'].pop('proxies', None)
                        kwargs['http_client'].pop('proxy', None)
                
                # Remove any other proxy-related keys (case insensitive)
                keys_to_remove = []
                for key in list(kwargs.keys()):
                    if 'proxy' in key.lower():
                        keys_to_remove.append(key)
                for key in keys_to_remove:
                    kwargs.pop(key, None)
                
                # Check nested structures
                for key, value in list(kwargs.items()):
                    if isinstance(value, dict):
                        for subkey in list(value.keys()):
                            if 'proxy' in subkey.lower():
                                value.pop(subkey, None)
            
            def _patched_client_init(self, *args, **kwargs):
                """Patched __init__ that removes proxies parameter."""
                # Clean all proxy-related parameters BEFORE calling original
                # This is critical - we must clean before Pydantic validation
                _clean_proxy_kwargs(kwargs)
                
                # Call original __init__ using stored reference
                if _original_client_init_stored is None:
                    raise RuntimeError("Original groq.Client.__init__ not stored")
                
                try:
                    return _original_client_init_stored(self, *args, **kwargs)
                except (TypeError, ValueError, Exception) as e:
                    error_str = str(e).lower()
                    # Check for any proxy-related errors
                    if any(keyword in error_str for keyword in ['proxies', 'unexpected keyword', 'proxy', 'type_error']):
                        # Clean again and retry
                        _clean_proxy_kwargs(kwargs)
                        try:
                            return _original_client_init_stored(self, *args, **kwargs)
                        except Exception as e2:
                            # If still fails, log and re-raise
                            print(f"⚠️ Error after cleaning proxies: {e2}")
                            raise
                    # Re-raise if it's not a proxy-related error
                    raise
            
            # Mark as patched
            _patched_client_init._groq_patch_applied = True
            
            # Apply patch to __init__
            groq.Client.__init__ = _patched_client_init
            
            # Also patch __new__ if it exists (critical for class instantiation)
            if _original_client_new_stored is not None and not hasattr(groq.Client.__new__, '_groq_patch_applied'):
                def _patched_client_new(cls, *args, **kwargs):
                    """Patched __new__ that removes proxies parameter."""
                    # Clean all proxy-related parameters BEFORE calling original
                    _clean_proxy_kwargs(kwargs)
                    try:
                        return _original_client_new_stored(cls, *args, **kwargs)
                    except (TypeError, ValueError, Exception) as e:
                        error_str = str(e).lower()
                        if any(keyword in error_str for keyword in ['proxies', 'unexpected keyword', 'proxy']):
                            # Clean again and retry
                            _clean_proxy_kwargs(kwargs)
                            return _original_client_new_stored(cls, *args, **kwargs)
                        raise
                
                _patched_client_new._groq_patch_applied = True
                groq.Client.__new__ = _patched_client_new
                print("✅ Patched groq.Client.__new__")
            
            _groq_client_patched = True
            print("✅ Patched groq.Client.__init__ and __new__")
            print(f"   - Original __init__: {_original_client_init_stored}")
            print(f"   - Original __new__: {_original_client_new_stored}")
            return True
        
    except (ImportError, AttributeError) as e:
        # groq might not be installed yet, that's okay
        pass
    except Exception as e:
        print(f"⚠️ Could not patch groq.Client: {e}")
    
    return False

# Try to patch immediately
_patch_groq_client()

# Global variable to store the original function and track if patched
_original_chatgroq_init_stored = None
_chatgroq_patched = False

# Function to patch langchain_groq - call this after importing langchain_groq
def patch_langchain_groq():
    """Patch langchain_groq.ChatGroq to remove proxies parameter."""
    global _original_chatgroq_init_stored, _chatgroq_patched
    
    # Ensure groq.Client is patched first
    _patch_groq_client()
    
    # Prevent multiple patches
    if _chatgroq_patched:
        return True
    
    try:
        import langchain_groq
        if hasattr(langchain_groq, 'ChatGroq'):
            # Check if already patched by checking if __init__ has our marker
            if hasattr(langchain_groq.ChatGroq.__init__, '_groq_patch_applied'):
                _chatgroq_patched = True
                return True
            
            # Store the ORIGINAL function before patching
            _original_chatgroq_init_stored = langchain_groq.ChatGroq.__init__
            
            def _patched_chatgroq_init(self, *args, **kwargs):
                """Patched ChatGroq.__init__ that removes proxies parameter."""
                # Be very aggressive in removing proxy-related parameters
                kwargs.pop('proxies', None)
                kwargs.pop('proxy', None)
                kwargs.pop('http_proxy', None)
                kwargs.pop('https_proxy', None)
                kwargs.pop('http_client', None)  # Remove http_client if it contains proxies
                
                # Also check for any nested proxy settings
                keys_to_remove = []
                for key in kwargs.keys():
                    if 'proxy' in key.lower():
                        keys_to_remove.append(key)
                for key in keys_to_remove:
                    kwargs.pop(key, None)
                
                # Check nested structures
                for key, value in list(kwargs.items()):
                    if isinstance(value, dict):
                        for subkey in list(value.keys()):
                            if 'proxy' in subkey.lower():
                                value.pop(subkey, None)
                
                # Use the stored original function (never the patched one)
                if _original_chatgroq_init_stored is None:
                    raise RuntimeError("Original ChatGroq.__init__ not stored. Patch may have failed.")
                
                try:
                    result = _original_chatgroq_init_stored(self, *args, **kwargs)
                    return result
                except (TypeError, ValueError) as e:
                    error_str = str(e).lower()
                    if 'proxies' in error_str or 'unexpected keyword' in error_str or 'proxy' in error_str:
                        # If error mentions proxies, try again without it
                        # Remove all possible proxy-related arguments
                        kwargs.pop('proxies', None)
                        kwargs.pop('proxy', None)
                        kwargs.pop('http_client', None)
                        keys_to_remove = []
                        for key in kwargs.keys():
                            if 'proxy' in key.lower() or 'http_client' in key.lower():
                                keys_to_remove.append(key)
                        for key in keys_to_remove:
                            kwargs.pop(key, None)
                        # Also check nested structures again
                        for key, value in list(kwargs.items()):
                            if isinstance(value, dict):
                                for subkey in list(value.keys()):
                                    if 'proxy' in subkey.lower():
                                        value.pop(subkey, None)
                        # Retry with cleaned kwargs
                        return _original_chatgroq_init_stored(self, *args, **kwargs)
                    raise
            
            # Mark the patch function
            _patched_chatgroq_init._groq_patch_applied = True
            
            # Apply the patch
            langchain_groq.ChatGroq.__init__ = _patched_chatgroq_init
            _chatgroq_patched = True
            print("✅ Patched langchain_groq.ChatGroq.__init__")
            print(f"   - Original ChatGroq.__init__ stored: {_original_chatgroq_init_stored is not None}")
            print(f"   - groq.Client patched: {_groq_client_patched}")
            
            # Also patch the _default_client method if it exists (only if not already patched)
            if hasattr(langchain_groq.ChatGroq, '_default_client'):
                if not hasattr(langchain_groq.ChatGroq._default_client, '_groq_patch_applied'):
                    _original_default_client_stored = langchain_groq.ChatGroq._default_client
                    
                    def _patched_default_client(*args, **kwargs):
                        # Remove all proxy-related parameters
                        kwargs.pop('proxies', None)
                        kwargs.pop('proxy', None)
                        kwargs.pop('http_client', None)
                        keys_to_remove = []
                        for key in kwargs.keys():
                            if 'proxy' in key.lower():
                                keys_to_remove.append(key)
                        for key in keys_to_remove:
                            kwargs.pop(key, None)
                        # Check nested structures
                        for key, value in list(kwargs.items()):
                            if isinstance(value, dict):
                                for subkey in list(value.keys()):
                                    if 'proxy' in subkey.lower():
                                        value.pop(subkey, None)
                        result = _original_default_client_stored(*args, **kwargs)
                        # If result is a dict with client creation, ensure proxies are removed
                        if isinstance(result, dict) and 'client' in result:
                            if hasattr(result['client'], '__init__'):
                                # The client should already be patched, but double-check
                                pass
                        return result
                    
                    _patched_default_client._groq_patch_applied = True
                    langchain_groq.ChatGroq._default_client = _patched_default_client
                    print("✅ Patched langchain_groq.ChatGroq._default_client")
            
            # Patch _get_client method if it exists (only if not already patched)
            if hasattr(langchain_groq.ChatGroq, '_get_client'):
                if not hasattr(langchain_groq.ChatGroq._get_client, '_groq_patch_applied'):
                    _original_get_client_stored = langchain_groq.ChatGroq._get_client
                    
                    def _patched_get_client(self, *args, **kwargs):
                        # Remove all proxy-related parameters
                        kwargs.pop('proxies', None)
                        kwargs.pop('proxy', None)
                        kwargs.pop('http_client', None)
                        keys_to_remove = []
                        for key in kwargs.keys():
                            if 'proxy' in key.lower():
                                keys_to_remove.append(key)
                        for key in keys_to_remove:
                            kwargs.pop(key, None)
                        # Check nested structures
                        for key, value in list(kwargs.items()):
                            if isinstance(value, dict):
                                for subkey in list(value.keys()):
                                    if 'proxy' in subkey.lower():
                                        value.pop(subkey, None)
                        return _original_get_client_stored(self, *args, **kwargs)
                    
                    _patched_get_client._groq_patch_applied = True
                    langchain_groq.ChatGroq._get_client = _patched_get_client
                    print("✅ Patched langchain_groq.ChatGroq._get_client")
            
            # Patch _client property or method if it exists
            # This is where langchain-groq might create the client
            if hasattr(langchain_groq.ChatGroq, '_client'):
                # Check if it's a property or method
                client_attr = getattr(langchain_groq.ChatGroq, '_client', None)
                if callable(client_attr) and not hasattr(client_attr, '_groq_patch_applied'):
                    _original_client_method_stored = client_attr
                    
                    def _patched_client_method(self, *args, **kwargs):
                        kwargs.pop('proxies', None)
                        kwargs.pop('proxy', None)
                        for key in list(kwargs.keys()):
                            if 'proxy' in key.lower():
                                kwargs.pop(key, None)
                        return _original_client_method_stored(self, *args, **kwargs)
                    
                    _patched_client_method._groq_patch_applied = True
                    setattr(langchain_groq.ChatGroq, '_client', _patched_client_method)
                    print("✅ Patched langchain_groq.ChatGroq._client method")
            
            return True
    except (ImportError, AttributeError) as e:
        print(f"⚠️ Could not patch langchain_groq: {e}")
    return False

# Try to patch if langchain_groq is already imported
try:
    patch_langchain_groq()
except Exception as e:
    print(f"⚠️ Error during initial patch: {e}")

