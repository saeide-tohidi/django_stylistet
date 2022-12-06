from django.contrib import admin
from django.utils.safestring import mark_safe

from backupp.models import BackupHistory


class BackupHistoryAdmin(admin.ModelAdmin):
    model = BackupHistory
    fields = [
        "name",
        "file",
        "download",
        "created_at",
        "updated_at",
    ]
    list_display = [
        "name",
        "file",
        "download",
        "created_at",
        "updated_at",
    ]
    readonly_fields = ["name", "file", "created_at", "updated_at", "download"]

    def download(self, obj):
        if obj.file:
            css = """
                    font-weight: normal;
                    font-size: 13px;
                    line-height: 1em;
                    display: inline-block;
                    padding: 0px 3px 0px 3px;
                    """

            html = """
                        <a href="{}" download style="{}">&nearr;</a>
                        """.format(
                obj.file.url, css
            )
            html = mark_safe(html)
            return html
        return "-"

    download.short_description = "download"


admin.site.register(BackupHistory, BackupHistoryAdmin)
