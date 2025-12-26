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

# Patch groq.Client to ignore proxies parameter
# This must be done BEFORE langchain_groq imports groq
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
        else:
            # Store the original before patching
            _original_client_init_stored = groq.Client.__init__
            
            def _patched_client_init(self, *args, **kwargs):
                """Patched __init__ that removes proxies parameter."""
                # Remove proxies if present
                kwargs.pop('proxies', None)
                # Also remove any nested proxy settings
                if 'http_client' in kwargs:
                    if isinstance(kwargs['http_client'], dict):
                        kwargs['http_client'].pop('proxies', None)
                # Remove any other proxy-related keys
                for key in list(kwargs.keys()):
                    if 'proxy' in key.lower():
                        kwargs.pop(key, None)
                # Call original __init__ using stored reference
                try:
                    if _original_client_init_stored is not None:
                        return _original_client_init_stored(self, *args, **kwargs)
                    else:
                        # Fallback (should not happen)
                        return object.__init__(self)
                except TypeError as e:
                    error_str = str(e).lower()
                    if 'proxies' in error_str or 'unexpected keyword' in error_str:
                        # Try one more time with all proxy-related args removed
                        for key in list(kwargs.keys()):
                            if 'proxy' in key.lower() or 'http_client' in key.lower():
                                kwargs.pop(key, None)
                        if _original_client_init_stored is not None:
                            return _original_client_init_stored(self, *args, **kwargs)
                        raise
                    raise
            
            # Mark as patched
            _patched_client_init._groq_patch_applied = True
            
            # Apply patch
            groq.Client.__init__ = _patched_client_init
            _groq_client_patched = True
            print("✅ Patched groq.Client.__init__")
    
except (ImportError, AttributeError) as e:
    # groq might not be installed yet, that's okay
    pass
except Exception as e:
    print(f"⚠️ Could not patch groq.Client: {e}")

# Global variable to store the original function and track if patched
_original_chatgroq_init_stored = None
_chatgroq_patched = False

# Function to patch langchain_groq - call this after importing langchain_groq
def patch_langchain_groq():
    """Patch langchain_groq.ChatGroq to remove proxies parameter."""
    global _original_chatgroq_init_stored, _chatgroq_patched
    
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
                # Remove proxies if present - do this multiple times to be safe
                kwargs.pop('proxies', None)
                kwargs.pop('http_client', None)  # Remove http_client if it contains proxies
                
                # Also check for any nested proxy settings
                for key in list(kwargs.keys()):
                    if 'proxy' in key.lower():
                        kwargs.pop(key, None)
                
                # Use the stored original function (never the patched one)
                if _original_chatgroq_init_stored is None:
                    raise RuntimeError("Original ChatGroq.__init__ not stored. Patch may have failed.")
                
                try:
                    result = _original_chatgroq_init_stored(self, *args, **kwargs)
                    return result
                except (TypeError, ValueError) as e:
                    error_str = str(e).lower()
                    if 'proxies' in error_str or 'unexpected keyword' in error_str:
                        # If error mentions proxies, try again without it
                        # Remove all possible proxy-related arguments
                        kwargs.pop('proxies', None)
                        kwargs.pop('http_client', None)
                        for key in list(kwargs.keys()):
                            if 'proxy' in key.lower() or 'http_client' in key.lower():
                                kwargs.pop(key, None)
                        # Retry with cleaned kwargs
                        return _original_chatgroq_init_stored(self, *args, **kwargs)
                    raise
            
            # Mark the patch function
            _patched_chatgroq_init._groq_patch_applied = True
            
            # Apply the patch
            langchain_groq.ChatGroq.__init__ = _patched_chatgroq_init
            _chatgroq_patched = True
            print("✅ Patched langchain_groq.ChatGroq.__init__")
            
            # Also patch the _default_client method if it exists (only if not already patched)
            if hasattr(langchain_groq.ChatGroq, '_default_client'):
                if not hasattr(langchain_groq.ChatGroq._default_client, '_groq_patch_applied'):
                    _original_default_client_stored = langchain_groq.ChatGroq._default_client
                    
                    def _patched_default_client(*args, **kwargs):
                        kwargs.pop('proxies', None)
                        kwargs.pop('http_client', None)
                        for key in list(kwargs.keys()):
                            if 'proxy' in key.lower():
                                kwargs.pop(key, None)
                        return _original_default_client_stored(*args, **kwargs)
                    
                    _patched_default_client._groq_patch_applied = True
                    langchain_groq.ChatGroq._default_client = _patched_default_client
                    print("✅ Patched langchain_groq.ChatGroq._default_client")
            
            # Patch _get_client method if it exists (only if not already patched)
            if hasattr(langchain_groq.ChatGroq, '_get_client'):
                if not hasattr(langchain_groq.ChatGroq._get_client, '_groq_patch_applied'):
                    _original_get_client_stored = langchain_groq.ChatGroq._get_client
                    
                    def _patched_get_client(self, *args, **kwargs):
                        kwargs.pop('proxies', None)
                        kwargs.pop('http_client', None)
                        for key in list(kwargs.keys()):
                            if 'proxy' in key.lower():
                                kwargs.pop(key, None)
                        return _original_get_client_stored(self, *args, **kwargs)
                    
                    _patched_get_client._groq_patch_applied = True
                    langchain_groq.ChatGroq._get_client = _patched_get_client
                    print("✅ Patched langchain_groq.ChatGroq._get_client")
            
            return True
    except (ImportError, AttributeError) as e:
        print(f"⚠️ Could not patch langchain_groq: {e}")
    return False

# Try to patch if langchain_groq is already imported
try:
    patch_langchain_groq()
except Exception as e:
    print(f"⚠️ Error during initial patch: {e}")

