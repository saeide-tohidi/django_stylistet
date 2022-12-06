from datetime import datetime
from django.contrib import messages
from django.core.management import call_command
from django.core.files import File
from django.http import HttpResponse, HttpResponseRedirect
from backupp.models import BackupHistory


def dump_view(request):
    filename = datetime.now().strftime("%y-%m-%d, %H:%M")
    output = open(f"dumpfile/{filename}.json", "w")
    call_command("dumpdata", format="json", indent=3, stdout=output)
    output.close()
    output = open(f"dumpfile/{filename}.json")
    backup = BackupHistory()
    backup.name = filename
    backup.file = File(output)
    backup.save()
    print("done")
    messages.success(request, "Backup saved")

    return HttpResponseRedirect("/admin/")
