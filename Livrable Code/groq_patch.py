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
    
except (ImportError, AttributeError) as e:
    # If groq is not available or patching fails, log but continue
    print(f"Warning: Could not patch groq.Client: {e}")

