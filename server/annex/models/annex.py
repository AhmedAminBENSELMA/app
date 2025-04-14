from django.db import models  

class Annex(models.Model):
    id = models.AutoField(primary_key=True)
    annex_type = models.CharField(max_length=50, blank=True, editable=False)
    user_name = models.CharField(max_length=100)
    inventory_no = models.CharField(max_length=50)
    applicator_no = models.CharField(max_length=50)
    leoni_terminal_no = models.CharField(max_length=50)
    supplier_terminal_no = models.CharField(max_length=50)

    date = models.DateField()




    class Meta:
        db_table = "annex"

    def save(self, *args, **kwargs):
        self.annex_type = self.__class__.__name__
        super().save(*args, **kwargs)



    def __str__(self):
        return f"{self.annex_type} {self.id}"