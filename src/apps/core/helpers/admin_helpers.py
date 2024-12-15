from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def get_admin_path(obj) -> str:
    return f"{reverse(f'admin:{obj._meta.app_label}_{obj._meta.model_name}_change', args=[obj.id])}"


def get_admin_reference(obj):
    path = get_admin_path(obj)
    return mark_safe(f'<a href="{path}">{obj}</a>')


def get_admin_image(obj, picture_field: str, size: int = 200):
    return format_html(f'<img src="{getattr(obj, picture_field).url}" width="auto" height="{size}px" />')
