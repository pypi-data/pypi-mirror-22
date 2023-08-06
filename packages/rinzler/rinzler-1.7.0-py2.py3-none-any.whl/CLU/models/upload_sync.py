# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models
from .upload import Upload


class UploadSync(models.Model):
    sync_cod = models.AutoField(primary_key=True)
    upload_cod = models.ForeignKey(Upload, models.DO_NOTHING, db_column='upload_cod')
    upload_sync = models.CharField(max_length=1)
    upload_sync_report = models.TextField(blank=True, null=True)
    upload_sync_status = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'upload_sync'
