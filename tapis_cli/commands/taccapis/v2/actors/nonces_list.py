from tapis_cli.display import Verbosity
from .mixins import ActorIdentifier

from . import API_NAME, SERVICE_VERSION
from .formatters import ActorsFormatMany
from .models import Nonce

__all__ = ['ActorsNoncesList']


class ActorsNoncesList(ActorsFormatMany, ActorIdentifier):
    """List the current nonces for an actor
    """
    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(ActorsNoncesList, self).get_parser(prog_name)
        parser = ActorIdentifier.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        actor_id = ActorIdentifier.get_identifier(self, parsed_args)
        results = self.tapis_client.actors.listNonces(actorId=actor_id)

        headers = self.render_headers(Nonce, parsed_args)
        records = []
        for rec in results:
            record = []
            for key in headers:
                val = self.render_value(rec.get(key, None))
                record.append(val)
            records.append(record)
        return (tuple(headers), tuple(records))