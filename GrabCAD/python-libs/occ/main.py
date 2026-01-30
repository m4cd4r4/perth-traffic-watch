
from cement import App, TestApp, init_defaults
from cement.core.exc import CaughtSignal
from .core.exc import OctaviaChickenCheckerError
from .controllers.base import Base
from .controllers.loadbalancer import LoadBalancer
import openstack

# configuration defaults
CONFIG = init_defaults('occ')
CONFIG['occ']['foo'] = 'bar'


def connect_to_openstack(app):
    app.log.info('Connecting to OpenStack')

    cloud = "default"

    app.extend('conn', openstack.connect(cloud=cloud))


def openstack_errors(app):
    app.log.info('Loading openstack exceptions')
    app.extend('err', openstack.exceptions)

class OctaviaChickenChecker(App):
    """Octavia Chicken Checker primary application."""

    class Meta:
        label = 'occ'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'print',
            'colorlog',
            'jinja2',
        ]

        # load hooks
        hooks = [
            ('post_setup', connect_to_openstack),
            ('post_setup', openstack_errors),
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # set the output handler
        output_handler = 'yaml'

        # register handlers
        handlers = [
            LoadBalancer
        ]


class OctaviaChickenCheckerTest(TestApp,OctaviaChickenChecker):
    """A sub-class of OctaviaChickenChecker that is better suited for testing."""

    class Meta:
        label = 'occ'


def main():
    with OctaviaChickenChecker() as app:
        try:
            app.run()

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except OctaviaChickenCheckerError as e:
            print('OctaviaChickenCheckerError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()
