from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.firewall.juniper.junos.command_templates import save_restore


class SaveRestoreActions(object):
    def __init__(self, cli_service, logger):
        """
        Save/restore configuration
        :param cli_service: config mode cli_service
        :type cli_service: CliService
        :param logger:
        :type logger: Logger
        :return:
        """
        self._cli_service = cli_service
        self._logger = logger

    def save_running(self, path):
        """
        Save running configuration
        :param path: Destination path
        :return:
        """
        output = CommandTemplateExecutor(self._cli_service, save_restore.SAVE).execute_command(dst_path=path)
        return output

    def restore_running(self, restore_type, path):
        """
        Restore running configuration
        :param restore_type: merge/override
        :param path: file source
        :return:
        """
        output = CommandTemplateExecutor(self._cli_service, save_restore.RESTORE).execute_command(
            restore_type=restore_type, src_path=path)
        return output
