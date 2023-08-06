
class Factory(object):

    def __init__(self, project):
        """Take in the project file."""

        self.project = project

    def entry_state(self):
        return State(self.project)


    ##############
    # Properties #
    ##############

    @property
    def project(self):
        return self.__project

    @project.setter
    def project(self, project):
        if type(project) is not Project:
            raise Exception("Invalid project of type {0}".format(type(project)))

        self.__project = project

from larissa.Project import Project
from larissa.State import State
