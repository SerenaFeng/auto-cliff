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
            self.conf = yaml.safe_load(cfd)

        pname = self.conf.get('project')
        if not self.conf.get('package'):
            self.conf.update({'package': pname.replace('-', '_')})
        if not self.conf.get('cli'):
            self.conf.update({'cli': pname})
        if not self.conf.get('entry-cls'):
            self.conf.update({
                'entry-cls': pname.replace('-', '').capitalize()
            })

        self.root_dir = parsed_args.output if parsed_args.output else './'
        self.pdir = os.path.join(self.root_dir, pname)
        self.env = Environment(loader=PackageLoader('cliff_generator',
                                                    'templates'))
        if os.path.exists(self.pdir) and parsed_args.rm:
            try:
                shutil.rmtree(self.pdir)
            except Exception as err:
                raise Exception('Delete project [{}] failed, '
                                'due to {}'.format(self.pdir, err))

        this_dir = os.path.dirname(os.path.realpath(__file__))
        self.templates_dir = os.path.join(os.path.dirname(this_dir),
                                          'templates/')

        print 'begin to create project [{}] tree'.format(pname)
        for root, dirs, files in os.walk(self.templates_dir):
            sr_dir = root.replace(self.templates_dir, '')
            dr_dir = sr_dir.format(**self.conf)
            dir = os.path.join(self.pdir, dr_dir)
            if not os.path.exists(dir):
                try:
                    os.makedirs(dir)
                except Exception as err:
                    raise Exception('Create dir [{}] failed, '
                                    'due to: {}'.format(dir, err))
            for file in files:
                if file == 'sub.py.j2':
                    self.render_subs(sr_dir, dr_dir)
                elif file.endswith('.j2'):
                    self.renderfile(file, sr_dir, dr_dir)
                elif not file.endswith('.pyc'):
                    if file in ('rest.py', 'url_parse.py') and \
                            not bool(self.conf.get('use_rest')):
                        continue

                    self.copyfile(file, sr_dir, dr_dir)

        return 'Congrats: Generate Success'

    def renderfile(self, filename, sr_dir, relative_dir):
        print 'begin to generate {}'.format(os.path.join(relative_dir, filename))
        template = self.env.get_template(os.path.join(sr_dir, filename))
        content = template.render(conf=self.conf)
        self.writefile(filename[:-3], content, relative_dir)

    def render_subs(self, sr_dir, relative_dir):
        for sub, actions in self.conf.get('subs').iteritems():
            print 'begin to render {}.py'.format(os.path.join(relative_dir, sub))
            template = self.env.get_template(os.path.join(sr_dir, 'sub.py.j2'))
            content = template.render(package=self.conf.get('package'),
                                      sub=sub,
                                      actions=actions)
            self.writefile('{}.py'.format(sub), content, relative_dir)

    def writefile(self, filename, content, relative_dir):
        fdir = os.path.join(self.pdir, relative_dir, filename)
        try:
            with open(fdir, 'w') as fd:
                fd.write(content)
        except Exception as err:
            print 'write file {} failed with: {}'.format(filename, err)

    def copyfile(self, filename, sr_dir, dr_dir):
        print 'begin to copy {}'.format(os.path.join(dr_dir, filename))
        src_dir = os.path.join(self.templates_dir, sr_dir, filename)
        dst_dir = os.path.join(self.pdir, dr_dir, filename)
        shutil.copyfile(src_dir, dst_dir)
