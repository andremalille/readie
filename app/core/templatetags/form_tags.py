from django import template
register = template.Library()


@register.filter(name='add_class')
def add_class(value, css_class):
    if hasattr(value, 'field') and hasattr(value, 'as_widget'):
        return value.as_widget(attrs={"class": css_class})
    else:
        return value


@register.filter(name='attr')
def attr(field, attr_args):
    attr_name, attr_value = attr_args.split(':')
    return field.as_widget(attrs={attr_name: attr_value})
