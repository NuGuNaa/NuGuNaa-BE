from django.contrib import admin
from .models import *


class DebateApplyCheck(admin.ModelAdmin):
    list_display = ('id', 'petition_id', 'email', 'position', 'raffle_check')

admin.site.register(Debate)
admin.site.register(Debate_Apply, DebateApplyCheck)