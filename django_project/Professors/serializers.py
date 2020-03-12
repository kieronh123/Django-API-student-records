from rest_framework import serializers
from .models import *


class ProfessorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professors
        fields = ['profID']


class ProfessorTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfessorTitle
        fields = ['profTitle']


class ModuleCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleCode
        fields = ['moduleID']


class ModuleNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleName
        fields = ['moduleID', 'moduleName']


class ModuleYearSemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModuleYearSemester
        fields = ['moduleID', 'moduleYear', 'moduleSemester']


class ModuleTaughtBySerializer(serializers.ModelSerializer):
    professor = ProfessorTitleSerializer(many=True)
    module = ModuleCodeSerializer(many=False)

    class Meta:
        model = ModulesTaughtBy
        fields = ['professor', 'module']


class RateProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RateProfessor
        fields = ['profID', 'moduleID', 'rating']
