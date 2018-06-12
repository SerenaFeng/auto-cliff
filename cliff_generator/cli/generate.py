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
        if not conf.get('cli'):
            conf.update({'cli': pname})

        root_dir = parsed_args.output if parsed_args.output else './'
        pdir = os.path.join(root_dir, pname)
        pkg_dir = os.path.join(pdir, package)
        cli_dir = os.path.join(pkg_dir, 'cli')
        utils_dir = os.path.join(pkg_dir, 'utils')

        print('begin generate project tree {}'.format(pkg_dir))
        if os.path.exists(pdir) and parsed_args.rm:
            try:
                shutil.rmtree(pdir)
            except Exception as err:
                raise Exception('Delete project [{}] failed, due to {}'.format(pdir, err))

        for dir in [cli_dir, utils_dir]:
            if not os.path.exists(dir):
                try:
                    os.makedirs(dir)
                except Exception as err:
                    raise Exception('Create dir [{}] failed, due to: {}'.format(dir, err))

        env = Environment(loader=PackageLoader('cliff_generator', 'templates'))

        for file in [('setup.py', pdir),
                     ('command.py', utils_dir),
                     ('gitignore', pdir, '.gitignore')]:
            print 'begin to generate {}/{}.py'.format(file[1], file[0])
            self.copyfile(*file)

        print 'begin to generate {}/setup.cfg'.format(pdir)
        setup_cfg_t = env.get_template('setup.cfg.j2')
        setup_cfg = setup_cfg_t.render(conf=conf)
        self.writefile('setup.cfg', setup_cfg, pdir)

        print 'begin to generate {}/shell.py'.format(pkg_dir)
        shell_py_t = env.get_template('shell.py.j2')
        shell_py = shell_py_t.render(conf=conf,
                                     cls=pname.replace('-', '').capitalize())
        self.writefile('shell.py', shell_py, pkg_dir)

        print 'begin to generate {}/__init__.py'.format(pkg_dir)
        for dir in [cli_dir, utils_dir, pkg_dir]:
            init_py_t = env.get_template('__init__.py.j2')
            init_py = init_py_t.render(author=conf.get('author'))
            self.writefile('__init__.py', init_py, dir)

        for sub, actions in conf.get('subs').iteritems():
            print 'begin to generate {}/{}.py'.format(cli_dir, sub)
            sub_py_t = env.get_template('sub.py.j2')
            sub_py = sub_py_t.render(package=package, sub=sub, actions=actions)
            self.writefile('{}.py'.format(sub), sub_py, cli_dir)

        return 'Congrats: Generate Success'

    def writefile(self, filename, content, dir):
        fdir = os.path.join(dir, filename)
        try:
            with open(fdir, 'w') as fd:
                fd.write(content)
        except Exception as err:
            print 'write file {} failed with: {}'.format(filename, err)

    def copyfile(self, filename, dst, dstname=None):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(os.path.dirname(this_dir), 'templates')
        shutil.copyfile(os.path.join(templates_dir, filename),
                        os.path.join(dst, filename if not dstname else dstname))
