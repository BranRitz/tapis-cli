from tapis_cli.display import Verbosity
from tapis_cli.clients.services.mixins import Username
from tapis_cli.commands.taccapis.model import Permission

from . import API_NAME, SERVICE_VERSION
from .formatters import MetadataFormatMany
from .mixins import MetadataUUID

__all__ = ['MetadataPemsRevoke']


class MetadataPemsRevoke(MetadataFormatMany, MetadataUUID, Username):

    HELP_STRING = 'Revoke Permissions on a Metadata document for a User'
    LEGACY_COMMMAND_STRING = 'metadata-pems-update'

    VERBOSITY = Verbosity.BRIEF
    EXTRA_VERBOSITY = Verbosity.RECORD

    def get_parser(self, prog_name):
        parser = super(MetadataPemsRevoke, self).get_parser(prog_name)
        parser = MetadataUUID.extend_parser(self, parser)
        parser = Username.extend_parser(self, parser)
        return parser

    def take_action(self, parsed_args):
        parsed_args = self.preprocess_args(parsed_args)
        identifier = MetadataUUID.get_identifier(self, parsed_args)

        body = {'username': parsed_args.username, 'permission': 'NONE'}
        revoke_result = self.tapis_client.meta.updateMetadataPermissions(
            uuid=identifier, body=body)

        headers = self.render_headers(Permission, parsed_args)
        results = self.tapis_client.meta.listMetadataPermissions(
            uuid=identifier)

        records = []
        for rec in results:
            record = []
            # Table display
            if self.app_verbose_level > self.VERBOSITY:
                record.append(rec.get('username'))
                record.extend(Permission.pem_to_row(rec.get('permission', {})))
            else:
                for key in headers:
                    val = self.render_value(rec.get(key, None))
                    record.append(val)
            # Deal with an API-side bug where >1 identical pems are
            # returned for the owning user when no additional pems have been
            # granted on the app
            if record not in records:
                records.append(record)

        return (tuple(headers), tuple(records))
