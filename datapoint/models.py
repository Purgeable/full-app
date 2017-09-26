# -*- coding: utf-8 -*-


from django.db import models


class Datapoint(models.Model):
    """
    Create table 'Datapoint' with fields:
      freq - a letter in 'aqmwd'
      name - string like 'VARNAME_unit', under 128 letters total
      date - date like '2017-01-31'
      value - float
    """
    ALLOWED_FREQUENCIES = (
        # (actial value, human-readable equivalent)
        ('a', 'annual'),
        ('q', 'quarterly'),
        ('m', 'monthly'),
        ('w', 'weekly'),
        ('d', 'daily')
    )

    freq = models.CharField(max_length=1, choices=ALLOWED_FREQUENCIES)
    name = models.CharField(max_length=128, null=False)
    date = models.DateField(null=False)
    value = models.FloatField(null=False)

    class Meta:
        unique_together = ('freq', 'name', 'date')        
