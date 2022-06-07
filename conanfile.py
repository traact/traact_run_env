from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans import ConanFile, CMake
from conans.tools import os_info
import os


class TraactVirtualRunEnvGenerator(VirtualRunEnvGenerator):

    def __init__(self, conanfile):
        super(TraactVirtualRunEnvGenerator, self).__init__(conanfile)
        self.venv_name = "traact_run_env"

    def traact_env_items(self):
        lib_paths = []
        for dep in self.conanfile.deps_cpp_info.deps:
            if (dep.startswith('traact') and (dep != 'traact_core')):
                if self.settings.os == "Windows":
                    lib_paths.extend(self.conanfile.deps_cpp_info[dep].bin_paths)
                else:
                    lib_paths.extend(self.conanfile.deps_cpp_info[dep].lib_paths)

        return lib_paths

    def _add_traact_plugins(self):
        self.env['TRAACT_PLUGIN_PATHS'] = self.traact_env_items()
        return

    @property
    def content(self):
        self._add_traact_plugins()
        return super(TraactVirtualRunEnvGenerator, self).content


class TraactGeneratorPackage(ConanFile):
    name = "traact_run_env"
    version = "1.0.0"
    url = "https://github.com/traact/traact_run_env"
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
