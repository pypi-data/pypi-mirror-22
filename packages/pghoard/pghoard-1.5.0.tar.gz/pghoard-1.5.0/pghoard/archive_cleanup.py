"""
pghoard: clean up unused WAL from archive

Copyright (c) 2017 Ohmu Ltd
See LICENSE for details
"""
from pghoard import common, config, logutil, version
from pghoard.rohmu import get_transfer
from pghoard.rohmu.errors import InvalidConfigurationError
import argparse
import logging
import os
import sys


class ArchiveCleanup:
    def __init__(self):
        self.log = logging.getLogger(self.__class__.__name__)
        self.config = None
        self.site = None
        self.backup_site = None
        self.storage = None

    def set_config(self, config_file, site):
        self.config = config.read_json_config_file(config_file, check_commands=False)
        self.site = config.get_site_from_config(self.config, site)
        self.backup_site = self.config["backup_sites"][self.site]
        storage_config = common.get_object_storage_config(self.config, self.site)
        self.storage = get_transfer(storage_config)

    def storage_path(self, name):
        return os.path.join(self.config["path_prefix"], self.site, name)

    def archive_cleanup(self):
        basebackups = self.storage.list_path(self.storage_path("basebackup"))
        first_required_wal = min(bb["metadata"]["start-wal-segment"] for bb in basebackups)
        self.log.info("First required WAL segment is %r", first_required_wal)
        for object_info in self.storage.list_iter(self.storage_path("xlog"), with_metadata=False):
            object_name = object_info["name"]
            segment = os.path.basename(object_name)
            if segment < first_required_wal:
                self.log.info("Orphan WAL segment %r needs to be deleted", segment)
                self.storage.delete_key(object_name)

    def run(self, args=None):
        parser = argparse.ArgumentParser()
        parser.add_argument("--version", action='version', help="show program version",
                            version=version.__version__)
        parser.add_argument("--site", help="pghoard site", required=False)
        parser.add_argument("--config", help="pghoard config file", default=os.environ.get("PGHOARD_CONFIG"))
        args = parser.parse_args(args)
        self.set_config(args.config, args.site)
        return self.archive_cleanup()


def main():
    logutil.configure_logging(level=logging.INFO)
    tool = ArchiveCleanup()
    try:
        return tool.run()
    except KeyboardInterrupt:
        print("*** interrupted by keyboard ***")
        return 1
    except InvalidConfigurationError as ex:
        tool.log.error("FATAL: %s: %s", ex.__class__.__name__, ex)
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
