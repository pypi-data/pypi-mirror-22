from django.conf import settings
from django.utils.translation import ugettext_lazy as _

__all__ = (
    'CONTENT_LABEL_CHOICES',
    'DETAIL_IMAGE_KWARGS',
    'DETAIL_IMAGE_PROCESSORS',
    'NEWS_CONTENT_BLOCKS',
    'PAGINATE_BY',
    'THUMBNAIL_IMAGE_KWARGS',
    'THUMBNAIL_IMAGE_PROCESSORS',
)

S = lambda n, d=None: getattr(settings, 'TOUCHTECHNOLOGY_NEWS_' + n, d) or d

DEFAULT_CONTENT_LABEL_CHOICES = (
    ('copy', _('Copy')),
)

DEFAULT_DETAIL_IMAGE_KWARGS = {}
DEFAULT_DETAIL_IMAGE_PROCESSORS = (
    ('pilkit.processors.resize.SmartResize', (320, 240), {}),
)

DEFAULT_THUMBNAIL_IMAGE_KWARGS = {}
DEFAULT_THUMBNAIL_IMAGE_PROCESSORS = (
    ('pilkit.processors.resize.SmartResize', (160, 120), {}),
)

CONTENT_LABEL_CHOICES = S('CONTENT_LABEL_CHOICES',
                          DEFAULT_CONTENT_LABEL_CHOICES)
DETAIL_IMAGE_KWARGS = S('DETAIL_IMAGE_KWARGS',
                        DEFAULT_DETAIL_IMAGE_KWARGS)
DETAIL_IMAGE_PROCESSORS = S('DETAIL_IMAGE_PROCESSORS',
                            DEFAULT_DETAIL_IMAGE_PROCESSORS)
NEWS_CONTENT_BLOCKS = S('CONTENT_BLOCKS', 1)
PAGINATE_BY = S('PAGINATE_BY', 5)
THUMBNAIL_IMAGE_KWARGS = S('THUMBNAIL_IMAGE_KWARGS',
                           DEFAULT_THUMBNAIL_IMAGE_KWARGS)
THUMBNAIL_IMAGE_PROCESSORS = S('THUMBNAIL_IMAGE_PROCESSORS',
                               DEFAULT_THUMBNAIL_IMAGE_PROCESSORS)
