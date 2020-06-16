from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans import ConanFile, CMake
from conans.tools import os_info
import os

class traact_virtualrunenv_generator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(traact_virtualrunenv_generator, self).__init__(conanfile)
        self.venv_name = "traactrunenv"

    def traact_env_items(self):
        lib_paths = []
        for dep in self.conanfile.deps_cpp_info.deps:
            if(dep.startswith('traact') and (dep != 'traact_core')):
                lib_paths.extend(self.conanfile.deps_cpp_info[dep].lib_paths)

        return lib_paths



    def _add_traact_plugins(self):

        traact_plugins = ''
        for plugin in self.traact_env_items():
            traact_plugins += '"%s":' % plugin

        traact_plugins = traact_plugins[:-1]


        self.env['TRAACT_PLUGIN_PATHS'] = self.traact_env_items()
        #print(self.env)

        return


    @property
    def content(self):
        self._add_traact_plugins()
        return super(traact_virtualrunenv_generator, self).content


class TraactGeneratorPackage(ConanFile):
    name = "traact_virtualrunenv_generator"
    version = "0.0.1"
    url = ""
    license = ""

    settings = "os", "compiler", "build_type", "arch"
    compiler = "cppstd"

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.includedirs = []
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []
        self.cpp_info.srcdirs = []