from django.contrib import admin

# Register your models here.

from ContestApp.models import (ContestModel, ContestResultModel, ResultModel, ContestResultConfigModel)


@admin.register(ContestModel)
class ContestInterfaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'id',)


@admin.register(ContestResultModel)
class ContestResultInterfaceAdmin(admin.ModelAdmin):
    list_display = ('contest', 'id', 'is_draft',)


@admin.register(ContestResultConfigModel)
class ContestResultConfigInterfaceAdmin(admin.ModelAdmin):
    list_display = ('contest_result', 'id',)


@admin.register(ResultModel)
class ResultInterfaceAdmin(admin.ModelAdmin):
    list_display = ('is_verified', 'inn', 'sum_pay', 'direction', 'ball', 'is_winner',)
    list_filter = ('is_verified', 'is_winner',)
    search_fields = ('inn', 'ogrn', 'sum_pay', 'request_sum_pay', 'ball', 'direction', 'org_name', 'project_name',)
