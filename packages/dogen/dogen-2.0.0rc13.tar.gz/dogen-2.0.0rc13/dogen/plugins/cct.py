import logging
import os
import yaml
import shutil

from dogen.plugin import Plugin


class CCT(Plugin):
    @staticmethod
    def info():
        return "cct", "Support for configuring images via CCT"

    def __init__(self, dogen, args):
        super(CCT, self).__init__(dogen, args)

    def extend_schema(self, parent_schema):
        """
        Read in a schema definition for our part of the config and hook it
        into the parent schema at the cct: top-level key.
        """
        schema_path = os.path.join(self.dogen.pwd, "schema", "cct_schema.yaml")
        schema = {}
        with open(schema_path, 'r') as fh:
            schema = yaml.safe_load(fh)

        parent_schema['map']['cct'] = schema

    def prepare(self, cfg):
        """
        create cct changes yaml file for image.yaml template decscriptor
        it require cct aware template.jinja file
        """
        # check if cct plugin has any steps to perform (prevent it from raising ugly exceptions)
        if 'cct' not in cfg:
            self.log.debug("No cct key in image.yaml - nothing to do")
            return

        # check if CCT is installed - complain otherwise
        # we are delaying import because CCT Plugin is not mandatory
        try:
            from cct.cli.main import CCT_CLI
        except ImportError:
            raise Exception("CCT plugin requires CCT to run - get it from https://github.com/containers-tools/cct")

        cfg['cct']['run'] = ['cct.yaml']

        cfg_file_dir = os.path.join(self.output, "cct")
        if not os.path.exists(cfg_file_dir):
            os.makedirs(cfg_file_dir)

        target_modules_dir = os.path.join(cfg_file_dir, 'modules')
        if os.path.exists(target_modules_dir):
            shutil.rmtree(target_modules_dir)
            self.log.debug('Removed existing modules directory: %s' % target_modules_dir)

        os.makedirs(target_modules_dir)

        cfg_file = os.path.join(cfg_file_dir, "cct.yaml")
        with open(cfg_file, 'w') as f:
            yaml.dump(cfg['cct']['configure'], f)

        # copy cct modules from
        modules_dir = os.path.join(os.path.dirname(self.descriptor), 'cct', 'modules')
        if os.path.exists(modules_dir):
            modules = filter(lambda x: os.path.isdir(os.path.join(modules_dir, x)), os.listdir(modules_dir))
            for module in modules:
                target_module = os.path.join(target_modules_dir, module)
                shutil.copytree(os.path.join(modules_dir, module), target_module)
                self.log.info("Copied module %s to %s" % (module, target_module))

        # setup cct to same logging level as dogen
        cct_logger = logging.getLogger("cct")
        cct_logger.setLevel(self.log.getEffectiveLevel())

        cct = CCT_CLI()
        cfg['artifacts'] = cct.fetch_artifacts([cfg_file], target_modules_dir, self.output)

        self.log.info("CCT plugin downloaded artifacts")

        cfg['entrypoint'] = ['/usr/bin/cct']

        if 'runtime' in cfg['cct']:
            self.runtime_changes(cfg)
            cfg['entrypoint'].append(cfg['cct']['runtime_changes'])

        cfg['entrypoint'].append("-c")

        if 'user' not in cfg['cct']:
            cfg['cct']['user'] = 'root'

    def runtime_changes(self, cfg):
        """
        Handle configuring CCT for runtime use.

        User may supply a /cct/runtime key which will be written out as
        instructions for cct to execute at runtime.
        """

        # write out a cctruntime.yaml file from the /cct/runtime_changes key
        cfg_file_dir = os.path.join(self.output, "cct")
        if not os.path.exists(cfg_file_dir):
            os.makedirs(cfg_file_dir)
        cfg_file = os.path.join(cfg_file_dir, "cctruntime.yaml")
        with open(cfg_file, 'w') as f:
            yaml.dump(cfg['cct']['runtime'], f)

        # adjust cfg object so caller adds the above to ENTRYPOINT
        if 'runtime_changes' not in cfg['cct']:
            cfg['cct']['runtime_changes'] = "/tmp/cct/cctruntime.yaml"
