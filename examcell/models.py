import datetime
import os
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
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


class TagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class ResultTypeTag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class ResultBranchTag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class ResultPatternYrTag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class ResultPatternTag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class ResultSemesterTag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class ResultExamMonthTag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class ResultYearTag(models.Model):
    name = models.CharField(max_length=64)
    objects = TagManager()

    def __str__(self):
        return self.name


class Result(models.Model):
    # sample : Revaluation Result BE (Mechanical Engg. R-2012)_Sem-VIII_CBGS_May-2019
    type = models.ForeignKey(ResultTypeTag, blank=False, on_delete=models.CASCADE,
                             help_text=_("ex. Regular, Revaluation"))
    year = models.ForeignKey(ResultYearTag, blank=False, on_delete=models.CASCADE, help_text=_("ex. FE, SE"))
    branch = models.ForeignKey(ResultBranchTag, blank=False, on_delete=models.CASCADE,
                               help_text=_("ex. Computer, Electrical"))
    pattern_year = models.ForeignKey(ResultPatternYrTag, blank=False, on_delete=models.CASCADE,
                                     help_text=_("ex. R-2012, R-2016"))
    semester = models.ForeignKey(ResultSemesterTag, blank=False, on_delete=models.CASCADE,
                                 help_text=_("ex. SemII, SemIV"))
    pattern = models.ForeignKey(ResultPatternTag, blank=False, on_delete=models.CASCADE,
                                help_text=_("ex. CBCS, CBGS"))
    exam_month = models.ForeignKey(ResultExamMonthTag, blank=False, on_delete=models.CASCADE,
                                   help_text=_("ex. DEC, MAY"))
    # ref : https://stackoverflow.com/questions/49051017/year-field-in-django
    exam_year = models.IntegerField(default=current_year(),
                                    validators=[MinValueValidator(2000), max_value_current_year])
    author = models.ForeignKey(User, default=User, on_delete=models.CASCADE, )

    result_file = models.FileField(default='', validators=[ext_validators], upload_to=get_file_path)
    is_active = models.BooleanField(
        help_text=_(
            "Tick to make this entry live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive entries whereas the general public aren't."
        ),
        default=True,
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
            [str(self.type), str(self.year), str(self.branch), str(self.pattern_yr), str(self.semester),
             str(self.pattern), str(self.exam_month),
             str(self.exam_year)])

    def is_published(self):
        """
        Return True if the entry is publicly accessible.
        """
        return self.is_active and self.pub_date <= timezone.now()

    is_published.boolean = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
