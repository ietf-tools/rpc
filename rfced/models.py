# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Approvals(models.Model):
    app_id = models.AutoField(primary_key=True)
    a48_id = models.IntegerField()
    name = models.CharField(max_length=120, db_collation='utf8mb4_general_ci', blank=True, null=True)
    approved = models.CharField(max_length=3)
    approved_date = models.DateField(blank=True, null=True)
    create_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'approvals'


class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(unique=True, max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)
    area_acronym = models.CharField(max_length=10, db_collation='utf8mb4_general_ci', blank=True, null=True)
    area_status = models.CharField(max_length=6)
    area_director_name = models.CharField(db_column='AREA_DIRECTOR_NAME', max_length=200, db_collation='utf8mb4_general_ci')  # Field name made lowercase.
    area_director_email = models.CharField(db_column='AREA_DIRECTOR_EMAIL', max_length=200, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    area_web_page = models.CharField(db_column='AREA_WEB_PAGE', max_length=200, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'area'


class AreaAssignments(models.Model):
    fk_area = models.IntegerField()
    fk_index = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'area_assignments'


class Auth48S(models.Model):
    a48_id = models.AutoField(primary_key=True)
    doc_id = models.CharField(db_column='doc-id', unique=True, max_length=10)  # Field renamed to remove unsuitable characters.
    status = models.CharField(max_length=9)
    start_date = models.DateTimeField()
    completion_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    awaiting_ad_approval = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'auth48s'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group_id', 'permission_id'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type_id = models.IntegerField()
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type_id', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user_id = models.IntegerField()
    group_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user_id', 'group_id'),)


class AuthUserUserPermissions(models.Model):
    user_id = models.IntegerField()
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user_id', 'permission_id'),)


class Clusters(models.Model):
    entry_key = models.AutoField(primary_key=True)
    cluster_id = models.CharField(max_length=10)
    draft_base = models.CharField(unique=True, max_length=200)
    anchored = models.CharField(max_length=7, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clusters'
        db_table_comment = 'The draft_base cannot be a FOREIGN KEY on index.'


class Counters(models.Model):
    name = models.CharField(primary_key=True, max_length=8)
    value = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'counters'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type_id = models.IntegerField(blank=True, null=True)
    user_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EditorAssignments(models.Model):
    assign_id = models.AutoField(primary_key=True)
    initials = models.CharField(max_length=2)
    doc_key = models.IntegerField()
    role_key = models.IntegerField()
    create_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editor_assignments'
        db_table_comment = 'Allow users to override editor validations so no initials FK'


class EditorRoles(models.Model):
    role_key = models.AutoField(primary_key=True)
    role_code = models.CharField(max_length=3)
    role_name = models.CharField(max_length=80, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editor_roles'


class Editors(models.Model):
    ed_key = models.AutoField(primary_key=True)
    initials = models.CharField(unique=True, max_length=2)
    name = models.CharField(max_length=80, blank=True, null=True)
    assignable = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'editors'


class Errata(models.Model):
    errata_id = models.AutoField(primary_key=True)
    rs_code = models.CharField(max_length=3, db_collation='utf8mb4_general_ci', blank=True, null=True)
    doc_id = models.CharField(db_column='doc-id', max_length=10, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field renamed to remove unsuitable characters.
    status_id = models.IntegerField()
    type_id = models.IntegerField()
    conv_format_check = models.CharField(max_length=3, db_collation='latin1_swedish_ci', blank=True, null=True)
    section = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    orig_text = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    correct_text = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    submitter_name = models.CharField(max_length=80, blank=True, null=True)
    submitter_email = models.CharField(max_length=120, db_collation='utf8mb4_general_ci', blank=True, null=True)
    notes = models.TextField(db_collation='utf8mb4_general_ci', blank=True, null=True)
    submit_date = models.DateField()
    posted_date = models.DateField(blank=True, null=True)
    verifier_id = models.IntegerField(blank=True, null=True)
    verifier_name = models.CharField(max_length=80, db_collation='utf8mb4_general_ci', blank=True, null=True)
    verifier_email = models.CharField(max_length=120, db_collation='utf8mb4_general_ci', blank=True, null=True)
    insert_date = models.DateTimeField()
    update_date = models.DateTimeField(blank=True, null=True)
    format = models.CharField(max_length=100, db_collation='utf8mb4_general_ci')

    class Meta:
        managed = False
        db_table = 'errata'
        db_table_comment = 'rs_code is tag to aid correcting converted CGI records'


class ErrataLog(models.Model):
    elog_id = models.AutoField(primary_key=True)
    errata_id = models.IntegerField()
    verifier_id = models.IntegerField(blank=True, null=True)
    verifier_name = models.CharField(max_length=80, blank=True, null=True)
    status_id = models.IntegerField()
    doc_id = models.CharField(db_column='doc-id', max_length=10)  # Field renamed to remove unsuitable characters.
    type_id = models.IntegerField()
    section = models.TextField(blank=True, null=True)
    orig_text = models.TextField(blank=True, null=True)
    correct_text = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    edit_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'errata_log'


class ErrataStatusCodes(models.Model):
    errata_status_id = models.AutoField(primary_key=True)
    errata_status_code = models.CharField(max_length=40)
    errata_status_text = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'errata_status_codes'


class ErrataTypeCodes(models.Model):
    errata_type_id = models.AutoField(primary_key=True)
    errata_type_code = models.CharField(max_length=10)
    errata_type_helptext = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'errata_type_codes'


class Index(models.Model):
    internal_key = models.AutoField(primary_key=True)
    draft = models.CharField(db_column='DRAFT', max_length=200, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    date_received = models.DateField(db_column='DATE_RECEIVED', blank=True, null=True)  # Field name made lowercase.
    time_out_date = models.DateField(db_column='TIME-OUT-DATE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    expedite_need_date = models.CharField(db_column='EXPEDITE_NEED_DATE', max_length=10, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    iesg_approved = models.CharField(db_column='IESG_APPROVED', max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=3, blank=True, null=True)  # Field name made lowercase.
    doc_id = models.CharField(db_column='DOC-ID', max_length=10, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    title = models.TextField(db_column='TITLE', db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    authors = models.CharField(db_column='AUTHORS', max_length=300, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    format = models.CharField(db_column='FORMAT', max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    char_count = models.CharField(db_column='CHAR-COUNT', max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    page_count = models.PositiveIntegerField(db_column='PAGE-COUNT', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    pub_status = models.CharField(db_column='PUB-STATUS', max_length=21, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    status = models.CharField(db_column='STATUS', max_length=21, blank=True, null=True)  # Field name made lowercase.
    email = models.TextField(db_column='EMAIL', db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    source = models.CharField(db_column='SOURCE', max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    doc_shepherd = models.CharField(db_column='DOC_SHEPHERD', max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    iesg_contact = models.CharField(db_column='IESG_CONTACT', max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    abstract = models.TextField(db_column='ABSTRACT', db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    pub_date = models.DateField(db_column='PUB-DATE', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    nroffed = models.CharField(db_column='NROFFED', max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    keywords = models.TextField(db_column='KEYWORDS', db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    organization = models.TextField(db_column='ORGANIZATION', db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    queries = models.CharField(db_column='QUERIES', max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    last_query = models.CharField(db_column='LAST-QUERY', max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    responses = models.CharField(db_column='RESPONSES', max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    last_response = models.CharField(db_column='LAST-RESPONSE', max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    notes = models.TextField(db_column='NOTES', db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    obsoletes = models.CharField(db_column='OBSOLETES', max_length=250, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    obsoleted_by = models.CharField(db_column='OBSOLETED-BY', max_length=250, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    updates = models.CharField(db_column='UPDATES', max_length=760, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    updated_by = models.CharField(db_column='UPDATED-BY', max_length=250, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    see_also = models.CharField(db_column='SEE-ALSO', max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    see_also_title = models.TextField(db_column='SEE-ALSO-TITLE', db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    ref = models.CharField(db_column='REF', max_length=600, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    ref_flag = models.IntegerField()
    iana_flag = models.IntegerField()
    state_id = models.IntegerField()
    generation_number = models.IntegerField()
    consensus_bit = models.CharField(max_length=3, blank=True, null=True)
    xml_file = models.IntegerField()
    doi = models.CharField(db_column='DOI', max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)  # Field name made lowercase.
    sub_page_count = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'index'


class OpNotes(models.Model):
    op_int_key = models.IntegerField()
    op_notes = models.TextField()

    class Meta:
        managed = False
        db_table = 'op_notes'


class ReportSources(models.Model):
    rs_code = models.CharField(primary_key=True, max_length=3)
    rs_description = models.CharField(max_length=180, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'report_sources'


class RpcRfcstatesummary(models.Model):
    old_iana_flag = models.IntegerField(blank=True, null=True)
    old_ref_flag = models.IntegerField(blank=True, null=True)
    old_version_number = models.IntegerField(blank=True, null=True)
    iana_flag = models.IntegerField(blank=True, null=True)
    ref_flag = models.IntegerField(blank=True, null=True)
    version_number = models.IntegerField(blank=True, null=True)
    days = models.PositiveSmallIntegerField()
    oldstate_id = models.IntegerField(blank=True, null=True)
    rfc_id = models.IntegerField()
    state_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rpc_rfcstatesummary'
        unique_together = (('rfc_id', 'oldstate_id', 'state_id', 'old_version_number', 'version_number', 'old_iana_flag', 'old_ref_flag', 'iana_flag', 'ref_flag'),)


class RpcStatebydate(models.Model):
    state_date = models.DateField()
    page_count = models.PositiveIntegerField()
    state_id = models.IntegerField()
    doc_count = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'rpc_statebydate'
        unique_together = (('state_id', 'state_date'),)


class SourceList(models.Model):
    rfc_number = models.CharField(max_length=7)
    wg_acronym = models.CharField(max_length=20, blank=True, null=True)
    draft_string = models.CharField(max_length=100, blank=True, null=True)
    wg_name = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_list'


class StateHistory(models.Model):
    internal_dockey = models.IntegerField()
    state_id = models.IntegerField()
    in_date = models.DateField()
    version_number = models.IntegerField(blank=True, null=True)
    iana_flag = models.IntegerField()
    ref_flag = models.IntegerField()
    generation_number = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'state_history'


class States(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'states'


class Statistics(models.Model):
    internal_key = models.IntegerField()
    weeks_in_state = models.DecimalField(max_digits=10, decimal_places=1)
    report_date = models.DateField()
    week_of_year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'statistics'


class StatusChanges(models.Model):
    dockey = models.IntegerField(primary_key=True)
    date_of_change = models.DateField(blank=True, null=True)
    url_of_change = models.TextField(db_column='URL_of_change', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'status_changes'


class StreamSpecificParties(models.Model):
    ssp_id = models.AutoField(primary_key=True)
    stream_name = models.CharField(max_length=126, blank=True, null=True)
    ssp_name = models.CharField(max_length=126, blank=True, null=True)
    ssp_email = models.CharField(max_length=126)
    ssp_webpage = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stream_specific_parties'


class Subcounts(models.Model):
    doc_id = models.CharField(db_column='doc-id', max_length=10)  # Field renamed to remove unsuitable characters.
    draft = models.CharField(max_length=200)
    sub_page_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'subcounts'


class TestPagecountData(models.Model):
    doc_id = models.CharField(db_column='DOC-ID', max_length=10)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    draft_name = models.CharField(db_column='DRAFT-NAME', max_length=180)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    draft_version = models.CharField(db_column='DRAFT-VERSION', max_length=20)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    page_count = models.CharField(db_column='PAGE-COUNT', max_length=50)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        managed = False
        db_table = 'test_pagecount_data'


class Verifiers(models.Model):
    verifier_id = models.AutoField(primary_key=True)
    ssp_id = models.IntegerField()
    login_name = models.CharField(max_length=80)
    password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'verifiers'


class WorkingGroup(models.Model):
    wg_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=50, db_collation='utf8mb4_general_ci', blank=True, null=True)
    wg_acronym = models.CharField(max_length=15, db_collation='utf8mb4_general_ci', blank=True, null=True)
    wg_name = models.CharField(max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)
    ssp_id = models.IntegerField()
    wg_chair_name = models.CharField(max_length=200, blank=True, null=True)
    wg_chair_email = models.CharField(max_length=200, db_collation='utf8mb4_general_ci', blank=True, null=True)
    wg_email = models.CharField(max_length=80, db_collation='utf8mb4_general_ci', blank=True, null=True)
    wg_status = models.CharField(max_length=5)
    other_areas = models.CharField(max_length=100, db_collation='utf8mb4_general_ci', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'working_group'
        unique_together = (('wg_name', 'area_name'),)
