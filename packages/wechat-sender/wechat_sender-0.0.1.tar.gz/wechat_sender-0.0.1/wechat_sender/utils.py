# coding: utf-8
from __future__ import unicode_literals
import codecs

STATUS_SUCCESS = 0
STATUS_PERMISSION_DENIED = 1
STATUS_BOT_EXCEPTION = 2


def _read_config_list():
    with codecs.open('conf.ini', 'w+', encoding='utf-8') as f1:
        conf_list = [conf for conf in f1.read().split('\n') if conf != '']
        return conf_list


def write_config(name, value):
    name = name.lower()
    new = True
    conf_list = _read_config_list()
    for i, conf in enumerate(conf_list):
        if conf.startswith(name):
            conf_list[i] = '{0}={1}'.format(name, value)
            new = False
            break
    if new:
        conf_list.append('{0}={1}'.format(name, value))

    with codecs.open('conf.ini', 'w+', encoding='utf-8') as f1:
        for conf in conf_list:
            f1.write(conf + '\n')
    return True


def read_config(name):
    name = name.lower()
    conf_list = _read_config_list()
    for conf in conf_list:
        if conf.startswith(name):
            return conf.split('=')[1].split('#')[0].strip()
    return None


class StatusWrapperMixin(object):
    status_code = STATUS_SUCCESS
    status_message = ''

    def write(self, chunk):
        context = {'status': self.status_code,
                   'message': chunk}
        super(StatusWrapperMixin, self).write(context)
