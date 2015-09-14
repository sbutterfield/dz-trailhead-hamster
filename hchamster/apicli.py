import cmd
import json
import pydoc
import sys


from requests.exceptions import RequestException


class ClientCmdWrapper(cmd.Cmd):
    prompt = '>'
    output = sys.stdout
    APIExceptionClass = RequestException

    def __init__(self, client):
        cmd.Cmd.__init__(self)
        self.client = client

    def output_help(self, method):
        self.output.write(pydoc.render_doc(method, title='%s'))

    def callcmd(self, method, args, kwargs):
        return method(*args, **kwargs)

    def postcmd(self, result, line):
        print result

    def __getattr__(self, attr):
        if attr.startswith('do_'):
            method = getattr(self.client, attr[3:])

            def wrapper(arg):
                args = arg.split()
                kwargs = dict(a.split('=') for a in args if '=' in a)
                args = [a for a in args if '=' not in a]
                return self.callcmd(method, args, kwargs)

            return wrapper

        elif attr.startswith('help_'):
            method = getattr(self.client, attr[5:])

            def wrapper():
                self.output_help(method)

            return wrapper

        raise AttributeError


class JSONRequestClientCmdWrapper(ClientCmdWrapper):
    def callcmd(self, method, args, kwargs):
        try:
            if self.client.session is None:
                self.client.login()
            return method(*args, **kwargs)
        except TypeError:
            self.output_help(method)
        except self.APIExceptionClass as e:
            print e, e.response.text
            return e.response

    def postcmd(self, result, line):
        try:
            json.dump(result, self.output, sort_keys=True, indent=4, separators=(',', ': '))
        except TypeError:
            self.output.write(result.text)

        print ''


def run(cmdcli, args=None):
    if args is None:
        args = sys.argv[1:]

    if args:
        line = ' '.join(args)
        result = cmdcli.onecmd(line)
        cmdcli.postcmd(result, line)
    else:
        cmdcli.cmdloop()
