from django.db import models
import uuid

# table with ten columns of type char(PostgreSQL)
class TestData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # hexa-decimal unique id of table
    column1 = models.CharField(max_length=50, null=True, blank=True)
    column2 = models.CharField(max_length=50, null=True, blank=True)
    column3 = models.CharField(max_length=50, null=True, blank=True)
    column4 = models.CharField(max_length=50, null=True, blank=True)
    column5 = models.CharField(max_length=50, null=True, blank=True)
    column6 = models.CharField(max_length=50, null=True, blank=True)
    column7 = models.CharField(max_length=50, null=True, blank=True)
    column8 = models.CharField(max_length=50, null=True, blank=True)
    column9 = models.CharField(max_length=50, null=True, blank=True)
    column10 = models.CharField(max_length=50, null=True, blank=True)
    random_encryptionNum = models.IntegerField(default=0, null=True)

    class Meta:
        # for admin panel view
        verbose_name_plural = 'Test Data'

    def __str__(self):
        return str(self.id)

class TaskName(models.Model):
    task_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        # for admin panel view
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return str(self.task_name)