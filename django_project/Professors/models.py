from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Professors(models.Model):
    profID = models.CharField(primary_key=True, max_length=3)

    def __str__(self):
        return '{}'.format(self.profID)


class ProfessorTitle(models.Model):
    profID = models.ForeignKey(Professors, on_delete=models.CASCADE)
    profTitle = models.CharField(max_length=30)

    class Meta:
        unique_together = (('profID', 'profTitle'),)

    def __str__(self):
        return '{} {}'.format(self.profID, self.profTitle)


class ModuleCode(models.Model):
    moduleID = models.CharField(max_length=3)

    class Meta:
        unique_together = ('moduleID',)

    def __str__(self):
        return '{}'.format(self.moduleID)


class ModuleName(models.Model):
    moduleID = models.ForeignKey(ModuleCode, on_delete=models.CASCADE)
    moduleName = models.CharField(max_length=30)

    class Meta:
        unique_together = (('moduleID', 'moduleName'),)

    def __str__(self):
        return '{} {}'.format(self.moduleID, self.moduleName)


class ModuleYearSemester(models.Model):
    moduleID = models.ForeignKey(ModuleCode, on_delete=models.CASCADE)
    moduleYear = models.CharField(max_length=4)
    moduleSemester = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])

    class Meta:
        unique_together = (("moduleID", "moduleYear", "moduleSemester"),)

    def __str__(self):
        return '{} {} {}'.format(self.moduleID, self.moduleYear, self.moduleSemester)


class ModulesTaughtBy(models.Model):
    moduleInfo = models.ForeignKey(ModuleYearSemester, on_delete=models.CASCADE)
    moduleProfessors = models.ManyToManyField(ProfessorTitle)

    def __str__(self):
        return '{} {}'.format(self.moduleInfo, self.moduleProfessors.all())


class RateProfessor(models.Model):
    profID = models.ForeignKey(Professors, on_delete=models.CASCADE)
    moduleInfo = models.ForeignKey(ModuleYearSemester, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return '{} {} {}'.format(self.profID, self.moduleInfo, self.rating)