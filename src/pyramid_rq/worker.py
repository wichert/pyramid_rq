import argparse
import sys
import rq
try:
    from transaction import get as get_transaction
    HAVE_TRANSACTION = True
except ImportError:
    HAVE_TRANSACTION = False
from pyramid.paster import bootstrap
from rq import Queue, Worker
from redis.exceptions import ConnectionError


class PyramidWorker(Worker):
    def __init__(self, environment, *a, **kw):
        super(PyramidWorker, self).__init__(*a, **kw)
        self.environment = environment

    def perform_job(self, job):
        self.procline('Initializing pyramid for %s from %s' % 
                (job.func_name, job.origin))
        try:
            super(PyramidWorker, self).perform_job(job)
            if HAVE_TRANSACTION:
                get_transaction.commit()
        except:
            if HAVE_TRANSACTION:
                get_transaction.abort()
            raise
        finally:
            self.environment['closer']()


def run(options):
    environment = bootstrap(options.config)
    settings = environment['registry'].settings
    if 'rq.redis' not in settings:
        print >> sys.stderr, 'Critical error: ' \
                'pyramid_rq not configured by application'
        sys.exit(1)
    with rq.Connection(environment['registry'].settings['rq.redis']):
        try:
            queues = map(Queue, options.queues)
            w = PyramidWorker(options.config, queues, name=options.name)
            w.work(burst=options.burst)
        except ConnectionError as e:
            print(e)


def main():  # pragma: no coverage
    parser = argparse.ArgumentParser(
            description='Perform regular cleanup tasks')
    parser.add_argument('config', metavar='<ini-file>',
            help='Configuration file (and optionally section)')
    parser.add_argument('--burst', '-b', action='store_true',
            default=False,
            help='Run in burst mode (quit after all work is done)')
    parser.add_argument('--name', '-n', default=None,
            help='Specify a different name')
    parser.add_argument('--verbose', '-v', action='store_true',
            default=False, help='Show more output')
    parser.add_argument('queues', nargs='*', default=['default'],
            help='The queues to listen on (default: \'default\')')
    options = parser.parse_args()
    run(options)


if __name__ == '__main__':  # pragma: no coverage
    sys.exit(main() or 0)
