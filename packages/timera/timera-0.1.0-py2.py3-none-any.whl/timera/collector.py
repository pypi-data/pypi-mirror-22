# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import time
import logging

__all__ = ['run_loop']

log = logging.getLogger(__name__)


def get_config_section(config, section):
    # return dict with config params
    d = {}
    options = config.options(section)
    for option in options:
        d[option] = config.get(section, option)
    return d


def get_run_list(config):
    from . import plugins
    plugin_names = [m for m in dir(plugins) if not m.startswith('_')]
    run_list = []
    sections = config.sections()
    for section in sections:
        plugin_name = section.split('_', 2)[0]
        if section.startswith(plugin_name + '_plugin_'):
            if plugin_name not in plugin_names:
                raise ValueError('invalid config section "%s": plugin not found' % section)
            d = dict(type=None, config=None)
            d['type'] = plugin_name
            d['config'] = get_config_section(config, section)
            run_list.append(d)
    return run_list


def enqueue_plugins(run_list, queue, config, timestamp):
    for plugin in run_list:
        item = {}
        item['config'] = config
        item['timestamp'] = timestamp
        item['plugin'] = plugin
        queue.put_nowait(item)


def run_loop(config):
    from . import threadio
    from . import util
    collect_interval = max(2, config.getint('main', 'collector.interval'))
    num_collect_threads = config.getint('main', 'collector.threads')
    run_list = get_run_list(config)
    log.info('found %d entries in config' % len(run_list))
    collect_queue = threadio.start_workers(num_collect_threads)
    while True:
        """
        Sleep until next collection interval.
        This is so the next run time and db timestamps are predictable, but also so regardless of 
        how many timers are configured, workers will complete their work and there will be at least 
        some sleep time.
        This means that depending on how many timers there are and how long their work takes, 
        we may not run every "collector.interval". This is ok and intended behavior; do the work and 
        then sleep until the next closest "collector.interval", i.e. don't just throw items on a queue 
        every interval and hope the workers can keep up.
        """
        now = time.gmtime()
        numerator = now.tm_sec if collect_interval <= 60 else (now.tm_min * 60) + now.tm_sec
        next_interval = collect_interval - (numerator % collect_interval)
        log.debug('sleeping %d seconds until next collection interval' % next_interval)
        time.sleep(next_interval)
        # create timestamp for this collection interval
        timestamp = util.get_unix_now()
        log.info('collection interval starting')
        enqueue_plugins(run_list, collect_queue, config, timestamp)
        # wait until queue is drained
        collect_queue.join()
        log.info('collection interval completed')
