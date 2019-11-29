import datetime
import os
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.models import User


def ext_validators(value):
    ext = '%s' % os.path.splitext(value.name)[-1]
    if ext.lower() not in ['.pdf']:
        message = _('Invalid format, please choose: %(ext)s' % {'ext': ['.pdf']})
        raise ValidationError(message)


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('media/result', filename)


class ResultQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self):
        return self.filter(is_active=True)

    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class Result(models.Model):
    # sample : Revaluation Result BE (Mechanical Engg. R-2012)_Sem-VIII_CBGS_May-2019
    type = models.CharField(choices=(('Regular', 'Regular'), ('Revaluation', 'Revaluation')), max_length=50)
    branch = models.CharField(choices=(), max_length=64)
    pattern_yr = models.CharField(choices=(), max_length=64)
    pattern = models.CharField(choices=(), max_length=64, help_text=_("ex. CBCS, CBGS"))
    semester = models.CharField(choices=(), max_length=64)
    exam_month = models.CharField(choices=(('DEC', 'DEC'), ('MAY', 'MAY')), max_length=10, help_text=_("ex. DEC, MAY"))
    # ref : https://stackoverflow.com/questions/49051017/year-field-in-django
    exam_year = models.IntegerField(validators=[MinValueValidator(2000), max_value_current_year])

    year = models.CharField(choices=(('FE', 'FE'), ('SE', 'SE'), ('TE', 'TE'), ('BE', 'BE')), max_length=50)
    slug = models.SlugField(max_length=48)
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE)
    result_file = models.FileField(default='', validators=[ext_validators], upload_to=get_file_path)
    is_active = models.BooleanField(
        help_text=_(
            "Tick to make this entry live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive entries whereas the general public aren't."
        ),
        default=False,
    )
    pub_date = models.DateTimeField(
        verbose_name=_("Publication date"),
        help_text=_(
            "For an entry to be published, it must be active and its "
            "publication date must be in the past."
        ),
    )
    objects = ResultQuerySet.as_manager()

    class Meta:
        db_table = 'exam_results'
        verbose_name_plural = 'result'
        ordering = ('-pub_date',)
        get_latest_by = 'pub_date'

    def __str__(self):
        return '-'.join(
            [self.type, self.year, self.branch, self.pattern_yr, self.semester, self.pattern, self.exam_month,
             str(self.exam_year)])

    def get_absolute_url(self):
        kwargs = {
            'year': self.pub_date.year,
            'month': self.pub_date.strftime('%b').lower(),
            'day': self.pub_date.strftime('%d').lower(),
            'slug': self.slug,
        }
        return reverse('result_entry', kwargs=kwargs)

    def is_published(self):
        """
        Return True if the entry is publicly accessible.
        """
        return self.is_active and self.pub_date <= timezone.now()

    is_published.boolean = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
