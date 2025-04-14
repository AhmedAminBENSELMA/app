from django.db import models  # <-- Add this line
import os
import uuid
from .annex import Annex
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

def annex_6a_image_upload(instance, filename):

    base, ext = os.path.splitext(filename)
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
    unique_id = uuid.uuid4().hex
    new_filename = f"{timestamp}_{unique_id}{ext}"
    return os.path.join("annex", "upload", "annex6a" , new_filename)






class Annex6a(Annex):
    terminal_no = models.CharField(max_length=50)
    applicator_supplier = models.CharField(max_length=100)
    
    drawing_revision = models.CharField(max_length=50)
    original_zwg = models.BooleanField(default=False)
    
    cable_type_supplier = models.CharField(max_length=50)
    cross_sectio = models.CharField(max_length=50)  # Note the spelling as in your template
    terminal_supplier = models.CharField(max_length=50)
    wire_type = models.CharField(max_length=50)
    leoni_wire_no = models.CharField(max_length=50)
    sws_supplier = models.CharField(max_length=100)
    vw_sws_no = models.CharField(max_length=50)
    leoni_sws_no = models.CharField(max_length=50)
    
    # Conditional Fields
    critical_part = models.BooleanField(default=False)
    intervention = models.BooleanField(null=True, blank=True)
    reason = models.CharField(max_length=255, null=True, blank=True)
    first_off_release = models.BooleanField(null=True, blank=True)
    
    # Original Crimpdaten
    original_ch = models.FloatField(null=True, blank=True)
    original_ch_plus = models.FloatField(null=True, blank=True)
    original_cw = models.FloatField(null=True, blank=True)
    original_cw_plus = models.FloatField(null=True, blank=True)
    original_ich = models.FloatField(null=True, blank=True)
    original_ich_plus = models.FloatField(null=True, blank=True)
    original_icw = models.FloatField(null=True, blank=True)
    original_icw_plus = models.FloatField(null=True, blank=True)
    
    # Measured Crimpdaten
    measured_ch = models.FloatField(null=True, blank=True)
    measured_cw = models.FloatField(null=True, blank=True)
    measured_ich = models.FloatField(null=True, blank=True)
    measured_icw = models.FloatField(null=True, blank=True)
    
    # Schliffbildbeurteilung (micrograph evaluation)
    s = models.BooleanField(default=False)
    n = models.BooleanField(default=False)
    vw = models.BooleanField(default=False)
    sg = models.BooleanField(default=False)
    
    # Analysis Parameters
    ch_should = models.FloatField(null=True, blank=True)
    ch_is = models.FloatField(null=True, blank=True)
    pull_force_ability_should = models.FloatField(null=True, blank=True)
    pull_force_ability_is = models.FloatField(null=True, blank=True)
    pull_force_should = models.FloatField(null=True, blank=True)
    pull_force_is = models.FloatField(null=True, blank=True)
    aw_should = models.FloatField(null=True, blank=True)
    aw_is = models.FloatField(null=True, blank=True)
    la_should = models.FloatField(null=True, blank=True)
    la_is = models.FloatField(null=True, blank=True)
    fa_should = models.FloatField(null=True, blank=True)
    fa_is = models.FloatField(null=True, blank=True)
    cfe_should = models.FloatField(null=True, blank=True)
    cfe_is = models.FloatField(null=True, blank=True)
    gh_should = models.FloatField(null=True, blank=True)
    gh_is = models.FloatField(null=True, blank=True)
    gb_should = models.FloatField(null=True, blank=True)
    gb_is = models.FloatField(null=True, blank=True)
    sb_should = models.FloatField(null=True, blank=True)
    sb_is = models.FloatField(null=True, blank=True)
    
    # Standards for Evaluation
    standard_1 = models.BooleanField(default=False)
    standard_2 = models.BooleanField(default=False)
    standard_3 = models.BooleanField(default=False)
    standard_4 = models.BooleanField(default=False)
    standard_5 = models.BooleanField(default=False)
    standard_6 = models.BooleanField(default=False)
    
    # Other Evaluations
    micrograph_release = models.BooleanField(default=False)
    qm_release = models.BooleanField(default=False)
    
    # Remarks (List of remarks)
    remarks = ArrayField(
        models.CharField(max_length=255),
        blank=True,
        default=list,
        help_text="List of remarks"
    )
    
    # Image Field
    image_field = models.ImageField(
        upload_to=annex_6a_image_upload,
        null=True,
        blank=True
    )
    
    def clean(self):
        # Enforce conditional logic:
        #   - If critical_part is True:
        #         * first_off_release must be provided (not None).
        #         * intervention and reason must be absent.
        #   - If critical_part is False:
        #         * first_off_release must not be provided.
        #         * Both intervention and reason must be provided.

        if self.critical_part:
            if self.first_off_release is None:
                raise ValidationError("For a critical part, 'first_off_release' must be provided.")
            if self.intervention is not None:
                raise ValidationError("For a critical part, 'intervention' should not be provided.")
            if self.reason:
                raise ValidationError("For a critical part, 'reason' should not be provided.")
        else:
            if self.first_off_release is not None:
                raise ValidationError("For a non-critical part, 'first_off_release' should not be provided.")
            if self.intervention is None:
                raise ValidationError("For a non-critical part, 'intervention' must be provided.")
            if not self.reason:
                raise ValidationError("For a non-critical part, 'reason' must be provided.")
    
    
    
    
    
    class Meta:
        db_table = "annex6a"
    
    
    
    
    def __str__(self):
        return f"Annex6a Report {self.id} - {self.inventory_no}"