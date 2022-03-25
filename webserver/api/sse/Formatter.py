
"""
This module is supposed to contain function for formatting messages. As of now, it only
contains one function.

Methods
-------
format_sse(data : st)
    Formats the message to SSE format
"""

def format_sse(data : str):
    """Format a message string into a SSE compliant string
    
    Parameters
    ----------
    data : str
        The message to format
        
    Returns
    -------
    The message formated to an SSE compliant string
    """
    msg = f'data: {data}\n\n'
    return msg