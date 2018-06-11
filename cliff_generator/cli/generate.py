import os
import shutil
import yaml
from jinja2 import Environment, PackageLoader

from cliff_generator import cli


class Generation(cli.Command):
    def get_parser(self, prog_name):
        parser = super(Generation, self).get_parser(prog_name)
        parser.add_argument('conf_file',
                            type=str,
                            help='config file in yaml')
        parser.add_argument('-rm',
                            action='store_true',
                            default=False,
                            help='whether to rm existed project dir or not')
        parser.add_argument('-o', '--output',
                            help='Directory to place generated project')
        return parser

    def take_action(self, parsed_args):

        with open(parsed_args.conf_file, 'r') as cfd:
            conf = yaml.safe_load(cfd)

        pname = conf.get('project')
        package = conf.get('package')
        if not package:
            package = pname.replace('-', '_')
            conf.update({'package': package})
        cliname = conf.get('cli')
        if not cliname:
            cliname = pname
            conf.update({'cli': pname})

        root_dir = parsed_args.output if parsed_args.output else './'
        pdir = os.path.join(root_dir, pname)
        pkg_dir = os.path.join(pdir, package)
        cli_dir = os.path.join(pkg_dir, 'cli')

        print('begin generate project tree {}'.format(cli_dir))
        if os.path.exists(pdir) and parsed_args.rm:
            try:
                shutil.rmtree(pdir)
            except Exception as err:
                raise Exception('Delete project [{}] failed, due to {}'.format(pdir, err))

        if not os.path.exists(cli_dir):
            try:
                os.makedirs(cli_dir)
            except Exception as err:
                raise Exception('Create dir [{}] failed, due to: {}'.format(dir, err))

        env = Environment(loader=PackageLoader('cliff_generator', 'templates'))

        print 'begin to generate {}/setup.cfg'.format(pdir)
        setup_cfg_t = env.get_template('setup.cfg.j2')
        setup_cfg = setup_cfg_t.render(conf=conf)
        self.write_file('setup.cfg', setup_cfg, pdir)

        print 'begin to generate {}/setup.py'.format(pdir)
        setup_py_t = env.get_template('setup.py.j2')
        setup_py = setup_py_t.render()
        self.write_file('setup.py', setup_py, pdir)

        print 'begin to generate {}/shell.py'.format(pkg_dir)
        shell_py_t = env.get_template('shell.py.j2')
        shell_py = shell_py_t.render(conf=conf,
                                     cls=pname.replace('-', '').capitalize())
        self.write_file('shell.py', shell_py, pkg_dir)

        print 'begin to generate {}/__init__.py'.format(pkg_dir)
        init_py_empty_t = env.get_template('__init__.py.empty.j2')
        init_py_empty = init_py_empty_t.render(author=conf.get('author'))
        self.write_file('__init__.py', init_py_empty, pkg_dir)

        print 'begin to generate {}/__init__.py'.format(cli_dir)
        init_py_t = env.get_template('__init__.py.j2')
        init_py = init_py_t.render()
        self.write_file('__init__.py', init_py, cli_dir)

        for sub, actions in conf.get('subs').iteritems():
            print 'begin to generate {}/{}.py'.format(cli_dir, sub)
            sub_py_t = env.get_template('sub.py.j2')
            sub_py = sub_py_t.render(package=package, sub=sub, actions=actions)
            self.write_file('{}.py'.format(sub), sub_py, cli_dir)

        return 'Congrats: Generate Success'

    def write_file(self, filename, content, dir):
        fdir = os.path.join(dir, filename)
        with open(fdir, 'w') as fd:
            fd.write(content)
