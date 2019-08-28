from tapis_cli.display import Verbosity
from tapis_cli.search import SearchWebParam
from tapis_cli.commands.taccapis import SearchableCommand

from . import API_NAME, SERVICE_VERSION
from .models import System
from .formatters import SystemsFormatOne, SystemsFormatMany

__all__ = ['SystemsList']


class SystemsList(SystemsFormatMany):
    """List registered Systems
    """
    VERBOSITY = Verbosity.BRIEF
    id_display_name = None

    def get_parser(self, prog_name):
        parser = super(SystemsFormatMany, self).get_parser(prog_name)
        return parser

    def take_action(self, parsed_args):
        super().take_action(parsed_args)
        self.requests_client.setup(API_NAME, SERVICE_VERSION)
        self.take_action_defaults(parsed_args)

        results = self.requests_client.get_data(params=self.post_payload)
        headers = System().get_headers(self.VERBOSITY)

        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))