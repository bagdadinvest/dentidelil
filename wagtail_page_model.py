# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class WagtailcorePage(models.Model):
    id = models.AutoField()
    path = models.CharField(unique=True, max_length=255)
    depth = models.PositiveIntegerField()
    numchild = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    live = models.BooleanField()
    has_unpublished_changes = models.BooleanField()
    url_path = models.TextField()
    seo_title = models.CharField(max_length=255)
    show_in_menus = models.BooleanField()
    search_description = models.TextField()
    go_live_at = models.DateTimeField(blank=True, null=True)
    expire_at = models.DateTimeField(blank=True, null=True)
    expired = models.BooleanField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    owner = models.ForeignKey('UsersUser', models.DO_NOTHING, blank=True, null=True)
    locked = models.BooleanField()
    latest_revision_created_at = models.DateTimeField(blank=True, null=True)
    first_published_at = models.DateTimeField(blank=True, null=True)
    live_revision = models.ForeignKey('WagtailcorePagerevision', models.DO_NOTHING, blank=True, null=True)
    last_published_at = models.DateTimeField(blank=True, null=True)
    draft_title = models.CharField(max_length=255)
    locked_at = models.DateTimeField(blank=True, null=True)
    locked_by = models.ForeignKey('UsersUser', models.DO_NOTHING, blank=True, null=True)
    translation_key = models.CharField(max_length=32)
    locale = models.ForeignKey('WagtailcoreLocale', models.DO_NOTHING)
    alias_of_id = models.IntegerField(blank=True, null=True)
    slug_en_gb = models.CharField(max_length=255, blank=True, null=True)
    slug_tr = models.CharField(max_length=255, blank=True, null=True)
    url_path_en_gb = models.TextField(blank=True, null=True)
    url_path_tr = models.TextField(blank=True, null=True)
    search_description_en_gb = models.TextField(blank=True, null=True)
    search_description_tr = models.TextField(blank=True, null=True)
    title_en_gb = models.CharField(max_length=255, blank=True, null=True)
    title_tr = models.CharField(max_length=255, blank=True, null=True)
    seo_title_en_gb = models.CharField(max_length=255, blank=True, null=True)
    seo_title_tr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wagtailcore_page'
        unique_together = (('translation_key', 'locale'),)
