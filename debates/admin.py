from django.contrib import admin
from .models import *


class DebateCheck(admin.ModelAdmin):
    list_display = ('id', 'petition_id', 'member_announcement_date', 'debate_date', 'debate_code_O', 'debate_code_X')



class DebateApplyCheck(admin.ModelAdmin):
    list_display = ('id', 'petition_id', 'email', 'position', 'raffle_check')

admin.site.register(Debate, DebateCheck)
admin.site.register(Debate_Apply, DebateApplyCheck)