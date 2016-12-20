#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

from __future__ import unicode_literals

from django.db import models, IntegrityError
from django.utils.translation import ugettext_lazy as _

from common.utils import signer, date_expired_default
from common.mixins import NoDeleteModelMixin

__all__ = ['UserGroup']


class UserGroup(NoDeleteModelMixin):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Name'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def has_member(self, user):
        if user in self.users.all():
            return True
        return False

    def delete(self):
        if self.name != 'Default':
            self.users.clear()
            return super(UserGroup, self).delete()
        return True

    class Meta:
        db_table = 'user_group'

    @classmethod
    def initial(cls):
        group, created = cls.objects.get_or_create(name='Default', comment='Default user group for all user',
                                                   created_by='System')
        return group

    @classmethod
    def generate_fake(cls, count=100):
        from random import seed, choice
        import forgery_py
        from . import User

        seed()
        for i in range(count):
            group = cls(name=forgery_py.name.full_name(),
                        comment=forgery_py.lorem_ipsum.sentence(),
                        created_by=choice(User.objects.all()).username)
            try:
                group.save()
            except IntegrityError:
                print('Error continue')
                continue