from django import forms

from django.template.loader import render_to_string

try:
    from django.utils.encoding import force_str as force_text
except ImportError:
    from django.utils.encoding import force_text

from django.utils.safestring import mark_safe

from django.conf import settings

try:
    from django.forms.utils import flatatt
except ImportError:
    from django.forms.util import flatatt

class RichTextEditorWidget(forms.Textarea):
    class Media:
        js = (
            settings.STATIC_URL + 'admin/ckeditor/ckeditor.js',
            settings.STATIC_URL + 'admin/ckeditor/adapters/jquery.js',
        )

    # Override version 1.11 with version 1.9 to fix compatibility
    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        attrs = dict(self.attrs, **kwargs)
        if extra_attrs:
            attrs.update(extra_attrs)
        return attrs

    def render(self, name, value, attrs={}, renderer=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(render_to_string('ckeditor/widget.html', {
            'final_attrs': flatatt(final_attrs),
            'value': force_text(value),
            'id': final_attrs['id'],
        }))

from django import forms
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldError

class CheckboxSelectMultipleWithSelectAll(forms.CheckboxSelectMultiple):

    _all_selected = False

    def render(self, *args, **kwargs):
        empty = False
        if not self.choices:
            empty = True
        has_id = kwargs and ("attrs" in kwargs) and ("id" in kwargs["attrs"])
        if not has_id:
            raise FieldError("id required")
        select_all_id = kwargs["attrs"]["id"] + "_all"
        select_all_name = args[0] + "_all"
        original = super(CheckboxSelectMultipleWithSelectAll, self).render(*args, **kwargs)
        template = get_template("checkboxselectmultiplewithselectall/widget.html")
        context = Context({"original_widget":original,
                           "select_all_id":select_all_id,
                           'select_all_name':select_all_name,
                           'all_selected':self._all_selected,
                           'empty':empty})
        return mark_safe(template.render(context))

    def value_from_datadict(self, *args, **kwargs):
        original = super(CheckboxSelectMultipleWithSelectAll, self).value_from_datadict(*args, **kwargs)
        select_all_name=args[2] + "_all"
        if select_all_name in args[0]:
            self._all_selected = True
        else:
            self._all_selected = False
        return original
