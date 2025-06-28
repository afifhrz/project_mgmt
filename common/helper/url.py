def reverse_with_query_string(viewname, params, query_params):
    """
    Generate a URL with query string parameters for a given view name.

    :param viewname: The name of the view to reverse.
    :param kwargs: Query string parameters to include in the URL.
    :return: A URL string with the specified query parameters.
    """
    from django.urls import reverse
    from urllib.parse import urlencode

    base_url = reverse(viewname, kwargs=params)
    query_string = urlencode(query_params)

    return f"{base_url}?{query_string}" if query_string else base_url
