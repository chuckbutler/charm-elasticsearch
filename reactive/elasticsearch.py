import os

from charms.reactive import (
    when,
    when_not,
    set_state,
    remove_state,
)

from charms import apt

from charmhelpers.core.hookenv import (
    log,
    config,
    status_set,
    resource_get,
)


@when_not('elasticsearch.installed')
def check_install_path():
    try:
        status_set('Checking for resources')
        deb = resource_get('deb')
    except Exception:
        message = 'Error fetching the elasticsearch deb resource.'
        log(message)
        status_set('blocked', message)
        return

    filesize = os.stat(deb).st_size
    if deb and filesize > 1000000:
        set_state('elasticsearch.deb-install')
        return

    set_state('elasticsearch.apt-install')


@when('elasticsearch.apt-install')
@when_not('apt.installed.elasticsearch')
def install_elasticsearch():
    status_set('Queuing dependencies for install')
    apt.queue_install(['elasticsearch'])


@when('apt.installed.elasticsearch')
@when_not('elasticsearch.configured')
def configure_elasticsearch():
    set_state('elasticsearch.configured')


@when('config.changed')
def reconfigure():
    remove_state('elasticsearch.configured')
