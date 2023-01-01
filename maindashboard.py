from django.utils.translation import gettext_lazy as _
from django.urls import reverse, reverse_lazy
from grappelli.dashboard import modules, Dashboard


class CustomIndexDashboard(Dashboard):
    def init_with_context(self, context):
        self.children.append(
            modules.ModelList(
                title="User",
                column=1,
                models=("account.models.User",),
            )
        )

        self.children.append(
            modules.ModelList(
                title="User token",
                column=1,
                models=("rest_framework.authtoken.models.*",),
            )
        )

        self.children.append(
            modules.ModelList(
                title="Product",
                column=1,
                models=("product.models.Product",),
            )
        )
        self.children.append(
            modules.LinkList(
                _("Costume product dashboard"),
                layout="inline",
                column=1,
                children=(
                    {
                        "title": "Product",
                        "url": reverse("product_list"),
                        "external": True,
                        "target": "_blank",
                    },
                ),
            )
        )

        self.children.append(
            modules.ModelList(
                title="Attribute",
                column=1,
                models=(
                    "attribute.models.Attribute",
                    "attribute.models.AttributeValue",
                    "product.models.ProductType",
                    "product.models.ProductCategory",
                    "product.models.ProductMedia",
                ),
            )
        )
        self.children.append(
            modules.ModelList(
                title="Collection",
                column=1,
                models=("collection.models.*",),
            )
        )

        self.children.append(
            modules.ModelList(
                title="Authentication and Authorization",
                column=1,
                models=("django.contrib.auth.models.*",),
            )
        )
        self.children.append(
            modules.ModelList(
                title="Backup",
                column=1,
                models=("backupp.models.*",),
            )
        )
        self.children.append(
            modules.LinkList(
                _("Backup"),
                layout="inline",
                column=1,
                children=(
                    {
                        "title": "Backup database",
                        "url": reverse("backup_dump"),
                        "external": True,
                    },
                    {
                        "title": "Backup images",
                        "url": reverse("backup_view"),
                        "external": True,
                    },
                ),
            )
        )

        # self.children.append(
        #     modules.AppList(
        #         _("Applications"),
        #         collapsible=True,
        #         column=1,
        #         css_classes=("collapse closed",),
        #     )
        # )
