from __future__ import absolute_import

from uuid import uuid4

from django.utils.translation import ugettext_lazy as _

from vishap import render_video

from nonefield.fields import NoneField

from fobi.base import FormElementPlugin

from . import UID
from .forms import ContentVideoForm

__title__ = 'fobi.contrib.plugins.form_elements.content.content_video.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('ContentVideoPlugin',)


class ContentVideoPlugin(FormElementPlugin):
    """Content video plugin."""

    uid = UID
    name = _("Content video")
    group = _("Content")
    form = ContentVideoForm

    def post_processor(self):
        """Process plugin data.

        Always the same.
        """
        self.data.name = "{0}_{1}".format(self.uid, uuid4())

    def get_form_field_instances(self, request=None, form_entry=None,
                                 form_element_entries=None, **kwargs):
        """Get form field instances."""
        width, height = self.data.size.split('x')

        field_kwargs = {
            'initial': '<div class="video-wrapper">{0}</div>'.format(
                render_video(self.data.url, width, height)
            ),
            'required': False,
            'label': '',
        }

        return [(self.data.name, NoneField, field_kwargs)]
