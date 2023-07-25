from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, viewnames, css_class='active', inactive_class='', *args, **kwargs):
    """
    Renders the given CSS class if the request path matches the path of the view.
    :param context: The context where the tag was called. Used to access the request object.
    :param viewnames: The name of the view or views separated by || (include namespaces if any).
    :param css_class: The CSS class to render.
    :param inactive_class: The CSS class to render if the views is not active.
    :return:
    """
    request = context.get('request')
    if request is None:
        # Can't work without the request object.
        return ''
    current_url_name = request.resolver_match.url_name
    namespaces = request.resolver_match.namespaces
    active = False
    views = viewnames.split('||')
    for view_name in views:
        namespace = None
        if ":" in view_name:
            namespace, view_name = view_name.split(":", 1)

        if not namespace or namespace in namespaces:
            active = current_url_name == view_name.strip()

        if active:
            break

    if active:
        return css_class

    return inactive_class
