from django.utils.translation import gettext_lazy as _
from jet.dashboard import modules
from jet.dashboard.dashboard import Dashboard


class CustomIndexDashboard(Dashboard):
    """
    This is the configuration for the custom dashboard of the admin using Django-Jet
    """

    columns = 3

    def init_with_context(self, context):
        """
        We will add to the dashboard 3 sections, the applications with the models,
        the urls section with access to the api documentation and the recent actions
        section
        :param context:
        :return:
        """
        self.available_children += (
            modules.LinkList,
            modules.ModelList,
            modules.RecentActions,
        )
        self.children += (
            modules.ModelList(_("Models"), column=0, order=0),
            modules.LinkList(
                _("Support"),
                children=[
                    {
                        "title": _("Django documentation"),
                        "url": "http://docs.djangoproject.com/",
                        "external": True,
                    },
                ],
                column=1,
                order=0,
            ),
            modules.LinkList(
                _("API documentation"),
                children=[
                    {
                        "title": "Swagger",
                        "url": "/api/schema/swagger-ui/",
                        "external": False,
                    },
                    {
                        "title": "Redoc",
                        "url": "/api/schema/redoc/",
                        "external": False,
                    },
                ],
                column=1,
                order=1,
            ),
            modules.RecentActions(_("Recent Actions"), 10, column=2, order=0),
        )
