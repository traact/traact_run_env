from conans.client.generators.virtualrunenv import VirtualRunEnvGenerator
from conans import ConanFile, CMake, tools
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


class TraactPackageCmake(object):
    """
    Base class for all traact libraries
    """
    generators = "cmake", "TraactVirtualRunEnvGenerator"
    major_version = "0"
    minor_version = "0"
    patch_version = "0"

    next_major_version = "1"

    options = {
        "shared": [True, False],
        "with_tests": [True, False],
        "trace_logs_in_release": [True, False]
    }

    default_options = {
        "shared": True,
        "with_tests": True,
        "trace_logs_in_release": True
    }

    def __init__(self, arg_1, arg_2, arg_3, arg_4, arg_5):
        self._options()
        super(TraactPackageCmake, self).__init__(arg_1, arg_2, arg_3, arg_4, arg_5)

    def set_version(self):
        git = tools.Git(folder=self.recipe_folder)
        branch_name = "%s" % (git.get_branch())
        if branch_name == "main":
            self.major_version = self.next_major_version
            self.minor_version = "0"
            self.patch_version = "0"
        elif branch_name.startswith("releases/"):
            version_string = branch_name[len("releases/"):]
            self.major_version, self.minor_version, self.patch_version = version_string.split(".")
        self.version = '{0}.{1}.{2}'.format(self.major_version, self.minor_version, self.patch_version)

    # TODO set shared option of depending traact libraries
    def traact_requires(self, lib_name, lib_version):
        user_channel = "traact/stable"
        if lib_version == "latest":
            user_channel = "traact/latest"
            lib_version = "{0}.0.0".format(self.next_major_version)
        self.requires("{0}/{1}@{2}".format(lib_name, lib_version, user_channel))

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.verbose = True

        def add_cmake_option(t_option, t_value):
            var_name = "{}".format(t_option).upper()
            value_str = "{}".format(t_value)
            var_value = "ON" if value_str == 'True' else "OFF" if value_str == 'False' else value_str
            cmake.definitions[var_name] = var_value

        for option, value in self.options.items():
            add_cmake_option(option, value)

        cmake.configure()
        return cmake

    def build(self):
        self._before_configure()
        cmake = self._configure_cmake()
        self._before_build(cmake)
        cmake.build()
        self._after_build()

    def package(self):
        cmake = self._configure_cmake()
        self._before_package(cmake)
        cmake.install()
        self._after_package()

    def package_info(self):
        self.cpp_info.libs = [self.name]
        self._after_package_info()

    def _options(self):
        pass

    def _before_configure(self):
        pass

    def _before_build(self, cmake):
        pass

    def _after_build(self):
        pass

    def _before_package(self, cmake):
        pass

    def _after_package(self):
        pass

    def _after_package_info(self):
        pass


class TraactGeneratorPackage(TraactPackageCmake, ConanFile):
    name = "traact_run_env"
    url = "https://github.com/traact/traact_run_env.git"
    license = "MIT"
    description = "conan virtual env generator for traact libraries with some utils for conan and cmake setup"

    exports_sources = "CMakeLists.txt", "cmake/*"

    def build(self):
        pass

    def package_info(self):
        self.cpp_info.libs = []
