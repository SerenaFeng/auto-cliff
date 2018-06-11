import os

from jinja2 import Environment, PackageLoader

from cliff_generator import cli
from cliff_generator import config


class Generation(cli.Command):
    def get_parser(self, prog_name):
        parser = super(Generation, self).get_parser(prog_name)
        # parser.add_argument('-n', '--name',
        #                     default='test-cliff',
        #                     help='Project name to be generated')
        # parser.add_argument('-p', '--package',
        #                     default='test_cliff',
        #                     help='Package name, substitute \- with \_ if not provided')
        parser.add_argument('-o', '--output',
                            help='Directory to place generated project')
        return parser

    def take_action(self, parsed_args):

        pname = config.project.get('name')
        package = config.project.get('package')
        if not package:
            package = pname.replace('-', '_')
            config.project.update({'package': package})
        root_dir = parsed_args.output if parsed_args.output else './'
        pdir = os.path.join(root_dir, pname)
        pkg_dir = os.path.join(pdir, package)
        cli_dir = os.path.join(pkg_dir, 'cli')

        # try:
        #     os.makedirs(cli_dir)
        # except Exception as err:
        #     raise Exception('Create dir [{}] failed, due to: '.format(dir, str(err)))

        env = Environment(loader=PackageLoader('cliff_generator', 'templates'))
        setup_cfg_t = env.get_template('setup.cfg.j2')
        setup_cfg = setup_cfg_t.render(project=config.project)
        self.write_file('setup.cfg', setup_cfg, pdir)

        setup_py_t = env.get_template('setup.py.j2')
        setup_py = setup_py_t.render()
        self.write_file('setup.py', setup_py, pdir)

        shell_py_t = env.get_template('shell.py.j2')
        shell_py = shell_py_t.render(project=config.project,
                                     cls=pname.replace('-', '').capitalize())
        self.write_file('shell.py', shell_py, pkg_dir)

        init_py_empty_t = env.get_template('__init__.py.empty.j2')
        init_py_empty = init_py_empty_t.render(author=config.project.get('author'))
        self.write_file('__init__.py', init_py_empty, pkg_dir)

        init_py_t = env.get_template('__init__.py.j2')
        init_py = init_py_t.render()
        self.write_file('__init__.py', init_py, cli_dir)

        for sub, actions in config.project.get('subs').iteritems():
            print 'begin to render sub {}'.format(sub)
            sub_py_t = env.get_template('sub.py.j2')
            sub_py = sub_py_t.render(package=package, sub=sub, actions=actions)
            self.write_file('{}.py'.format(sub), sub_py, cli_dir)

        return 'success'

    def write_file(self, filename, content, dir):
        fdir = os.path.join(dir, filename)
        print content
        with open(fdir, 'w') as fd:
            fd.write(content)
