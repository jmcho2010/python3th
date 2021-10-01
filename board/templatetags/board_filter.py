from django import template

# 21.09.27 조준모 템플릿 태그 커스터마이징
register = template.Library()

@register.filter
def sub(value, arg):
    return value - arg