from __future__ import absolute_import

from django.forms.extras.widgets import SelectDateWidget
from django.forms.fields import DateField
from django.utils.translation import ugettext_lazy as _

from fobi.base import FormFieldPlugin, get_theme

from . import UID
from .forms import DateDropDownInputForm

__title__ = 'fobi.contrib.plugins.form_elements.fields.' \
            'date_drop_down.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('DateDropDownInputPlugin',)


theme = get_theme(request=None, as_instance=True)


class DateDropDownInputPlugin(FormFieldPlugin):
    """Date drop down field plugin."""

    uid = UID
    name = _("Date drop down")
    group = _("Fields")
    form = DateDropDownInputForm

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):
        """Get form field instances."""
        widget_attrs = {
            'class': theme.form_element_html_class,
            'type': 'date',
        }

        years = None
        if self.data.year_min and self.data.year_max:
            years = range(self.data.year_min, self.data.year_max)

        field_kwargs = {
            'label': self.data.label,
            'help_text': self.data.help_text,
            'initial': self.data.initial,
            # 'input_formats': self.data.input_formats,
            'required': self.data.required,
            'widget': SelectDateWidget(attrs=widget_attrs, years=years),
        }
        # if self.data.input_formats:
        #     kwargs['input_formats'] = self.data.input_formats

        return [(self.data.name, DateField, field_kwargs)]
