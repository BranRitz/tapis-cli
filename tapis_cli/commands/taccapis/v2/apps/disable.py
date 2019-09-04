from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.clients.services.mixins import ServiceIdentifier

from . import API_NAME, SERVICE_VERSION
from .models import App
from .formatters import AppsFormatOne

__all__ = ['AppsDisable']


class AppsDisable(ServiceIdentifier, AppsFormatOne):
    """Disable an app for usage
    """
    VERBOSITY = Verbosity.LISTING
    EXTRA_VERBOSITY = Verbosity.RECORD

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        headers = App().get_headers(self.VERBOSITY, parsed_args.formatter)
        rec = self.tapis_client.apps.manage(appId=parsed_args.identifier,
                                            body={'action': 'disable'})
        data = []
        for key in headers:
            val = self.render_value(rec.get(key, None))
            data.append(val)
        return (tuple(headers), tuple(data))