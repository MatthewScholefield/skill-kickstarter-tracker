from __builtin__ import unicode
from adapt.intent import IntentBuilder
from os.path import abspath, dirname, join

from mycroft import MycroftSkill, intent_handler
from mycroft.util import LOG

import sys
sys.path += [join(dirname(abspath(__file__)), 'PyKickstarter')]  # noqa
from PyKickstarter import PyKickstarter


class KickstarterTrackerSkill(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.kick = PyKickstarter()

    def get_level(self, project):
        gen = self.kick.search_projects(project).next()
        try:
            proj = next(gen)
        except StopIteration:
            raise ValueError
        for i in proj.data:
            if type(i) in [str, unicode]:
                try:
                    return float(i)
                except ValueError:
                    pass
        raise ValueError

    @intent_handler(IntentBuilder('').require('Project'))
    def handle_kickstarter_tracker(self, message):
        try:
            name = message.data.get("Project")
            level = self.get_level(name)
            self.speak_dialog('current.level', {'name': name, 'level': level})
        except ValueError:
            self.speak_dialog('not.found')


def create_skill():
    return KickstarterTrackerSkill()

