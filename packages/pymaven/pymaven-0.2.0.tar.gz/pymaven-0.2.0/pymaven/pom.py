#
# Copyright (c) SAS Institute Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import itertools
import logging
import re

from lxml import etree

from .artifact import Artifact
from .utils import memoize
from .versioning import VersionRange


POM_PARSER = etree.XMLParser(
    recover=True,
    remove_comments=True,
    remove_pis=True,
    )
PROPERTY_RE = re.compile(r'\$\{(.*?)\}')
STRIP_NAMESPACE_RE = re.compile(r"<project(.|\s)*?>")

log = logging.getLogger(__name__)


class Pom(Artifact):
    """Parse a pom file into a python object
    """

    RANGE_CHARS = ('[', '(', ']', ')')

    __slots__ = ("_client", "_parent", "_dep_mgmt", "_dependencies",
                 "_properties", "_xml")

    def __init__(self, coordinate, client):
        super(Pom, self).__init__(coordinate)
        with client.get_artifact(self.coordinate).contents as fh:
            xml = fh.read()
        self._xml = etree.fromstring(
            STRIP_NAMESPACE_RE.sub('<project>', xml[xml.find('<project'):], 1),
            parser=POM_PARSER,
            )
        self._client = client

        # dynamic attributes
        self._parent = None
        self._dep_mgmt = None
        self._dependencies = None
        self._properties = None

    def _find_deps(self, xml=None):
        if xml is None:
            xml = self._xml
        dependencies = {}

        # find all non-optional, compile dependencies
        for elem in xml.findall("dependencies/dependency"):
            group = self._replace_properties(elem.findtext("groupId"))
            artifact = self._replace_properties(elem.findtext("artifactId"))

            if (group, artifact) in self.dependency_management:
                version, scope, optional = \
                    self.dependency_management[(group, artifact)]
            else:
                version = scope = optional = None

            if elem.findtext("optional") is not None:
                optional = (elem.findtext("optional") == "true")
            else:
                optional = False

            if elem.findtext("version") is not None:
                version = elem.findtext("version")

            if version is None:
                # FIXME: Default to the latest released version if no
                # version is specified. I'm not sure if this is the
                # correct behavior, but let's try it for now.
                version = 'latest.release'
            else:
                version = self._replace_properties(version)

            if elem.findtext("scope") is not None:
                scope = elem.findtext("scope")

            # if scope is None, then it should be "compile"
            if scope is None:
                scope = "compile"

            dependencies.setdefault(scope, set()).add(
                ((group, artifact, version), not optional))

        return dependencies

    def _find_dependency_management(self, xml=None):
        if xml is None:
            xml = self._xml
        dep_mgmt = {}
        import_mgmt = {}

        for elem in xml.findall(
                "dependencyManagement/dependencies/dependency"):
            group = self._replace_properties(elem.findtext("groupId"))
            artifact = self._replace_properties(elem.findtext("artifactId"))
            version = self._replace_properties(elem.findtext("version"))

            scope = elem.findtext("scope")
            optional = (elem.findtext("optional") == "true")
            if scope is not None and scope == "import":
                import_pom = self._pom_factory(group, artifact, version)
                import_mgmt.update(import_pom.dependency_management)
            dep_mgmt[(group, artifact)] = (version, scope, optional)

        import_mgmt.update(dep_mgmt)
        return import_mgmt

    def _find_import_deps(self):
        dependencies = {}
        # process dependency management to find imports
        for group, artifact in self.dependency_management:
            version, scope, optional = \
                self.dependency_management[(group, artifact)]
            if scope == "import":
                dependencies.setdefault(scope, set()).add(
                    ((group, artifact, version), not optional))

        return dependencies

    def _find_prerequisites(self):
        properties = {}
        # get prerequisites
        prereqs = self._xml.find("prerequisites")
        if prereqs is not None:
            for elem in prereqs:
                properties['prerequisites.' + elem.tag] = elem.text
                properties['project.prerequisites.' + elem.tag] = elem.text

        return properties

    def _find_profiles(self):
        active_profiles = []
        default_profiles = []
        for p in self._xml.findall("profiles/profile"):
            if p.findtext("activation/activeByDefault") == "true":
                default_profiles.append(p)
            else:
                jdk = p.findtext("activation/jdk")
                if jdk is not None:
                    # attempt some clean up
                    if (jdk.startswith('[') or jdk.startswith("![")) \
                            and jdk.endswith(','):
                        # assume they left off the )
                        jdk += ')'

                    # TODO: make the JDK version selectable
                    if jdk.startswith('!'):
                        vr = VersionRange.fromstring(jdk[1:])
                        if (vr.version and "1.8" != vr.version) \
                                or (not vr.version and "1.8" not in vr):
                            active_profiles.append(p)
                    else:
                        vr = VersionRange.fromstring(jdk)
                        if (vr.version and "1.8" == vr.version) \
                                or (not vr.version and "1.8" in vr):
                            active_profiles.append(p)

        if active_profiles:
            return active_profiles
        else:
            return default_profiles

    def _find_properties(self, xml=None):
        if xml is None:
            xml = self._xml
        properties = {}
        project_properties = xml.find('properties')
        if project_properties is not None:
            for prop in project_properties.iterchildren():
                if prop.tag == 'property':
                    name = prop.get('name')
                    value = prop.get('value')
                else:
                    name = prop.tag
                    value = prop.text
                properties[name] = value
        return properties

    def _find_relocations(self, xml=None):
        if xml is None:
            xml = self._xml
        dependencies = {}
        # process distributionManagement for relocation
        relocation = xml.find("distributionManagement/relocation")
        if relocation is not None:
            group = relocation.findtext("groupId")
            if group is None:
                group = self.group_id
            else:
                group = self._replace_properties(group)

            artifact = relocation.findtext("artifactId")
            if artifact is None:
                artifact = self.artifact_id
            else:
                artifact = self._replace_properties(artifact)

            version = relocation.findtext("version")
            if version is None:
                version = self.version
            else:
                version = self._replace_properties(version)

            dependencies.setdefault("relocation", set()).add(
                ((group, artifact, version), True))

        return dependencies

    def _pom_factory(self, group, artifact, version):
        return Pom("%s:%s:pom:%s" % (group, artifact, version), self._client)

    def _replace_properties(self, text, properties=None):
        if properties is None:
            properties = self.properties

        def subfunc(matchobj):
            key = matchobj.group(1)
            return properties.get(key)

        result = PROPERTY_RE.sub(subfunc, text)
        while result and PROPERTY_RE.match(result):
            result = PROPERTY_RE.sub(subfunc, result)

        if not result:
            result = text
        return result.strip()

    def pick_version(self, spec, artifacts):
        """Pick a version from *versions* according to the spec

        Convert spec into maven version range and return the first version in
        *versions* that is within the range.

        :param str spec: a maven version range spec or gradle dynamic version
        :param versions: list of available versions for this artifact
        :type versions: [:py:class:`pymaven.Version`, ...]
        :return: the newest version that matches the spec
        :rtype: str or None
        """
        if spec in ("latest.release", "release"):
            for a in artifacts:
                if 'snapshot' not in str(a.version.version).lower():
                    return str(a.version)
        elif spec in ("latest.integration", "latest"):
            return str(artifacts[0].version)

        range = VersionRange.fromstring(spec)
        for artifact in artifacts:
            if artifact.version in range:
                return str(artifact.version)

    @property
    @memoize("_dependencies")
    def dependencies(self):
        dependencies = {}

        # we depend on our parent
        if self.parent is not None:
            group = self.parent.group_id
            artifact = self.parent.artifact_id
            version = self.parent.version
            dependencies.setdefault("compile", set()).add(
                ((group, artifact, str(version)), True))

        for key, value in itertools.chain(
                self._find_import_deps().iteritems(),
                self._find_deps().iteritems(),
                self._find_relocations().iteritems()):
            dependencies.setdefault(key, set()).update(value)

        for profile in self._find_profiles():
            for key, value in itertools.chain(
                    self._find_deps(profile).iteritems(),
                    self._find_relocations(profile).iteritems()):
                dependencies.setdefault(key, set()).update(value)

        return dependencies

    @property
    @memoize("_dep_mgmt")
    def dependency_management(self):
        dep_mgmt = {}

        # add parent's block first so we can override it
        if self.parent is not None:
            dep_mgmt.update(self.parent.dependency_management)

        dep_mgmt.update(self._find_dependency_management())
        for profile in self._find_profiles():
            dep_mgmt.update(self._find_dependency_management(profile))

        return dep_mgmt

    @property
    @memoize("_parent")
    def parent(self):
        parent = self._xml.find("parent")
        if parent is not None:
            group = parent.findtext("groupId").strip()
            artifact = parent.findtext("artifactId").strip()
            version = parent.findtext("version").strip()
            return self._pom_factory(group, artifact, version)

    @property
    @memoize("_properties")
    def properties(self):
        properties = {}

        if self.parent is not None:
            properties.update(self.parent.properties)
            properties['parent.groupId'] = self.parent.group_id
            properties['parent.artifactId'] = self.parent.artifact_id
            properties['parent.version'] = str(self.parent.version)
            properties['project.parent.groupId'] = self.parent.group_id
            properties['project.parent.artifactId'] = self.parent.artifact_id
            properties['project.parent.version'] = str(self.parent.version)

        # built-in properties
        properties['artifactId'] = self.artifact_id
        properties['groupId'] = self.group_id
        properties['version'] = str(self.version)
        properties['project.artifactId'] = self.artifact_id
        properties['project.groupId'] = self.group_id
        properties['project.version'] = str(self.version)
        properties['pom.artifactId'] = self.artifact_id
        properties['pom.groupId'] = self.group_id
        properties['pom.version'] = str(self.version)

        properties.update(self._find_properties())
        properties.update(self._find_prerequisites())

        for profile in self._find_profiles():
            profile_properties = profile.find("properties")
            if profile_properties is not None:
                for prop in profile_properties.iterchildren():
                    properties[prop.tag] = prop.text
        return properties

    def get_dependencies(self):
        return set(self.iter_dependencies())

    def get_build_dependencies(self):
        return set(self.iter_build_dependencies())

    def iter_dependencies(self):
        return itertools.chain(*self.dependencies.values())

    def iter_build_dependencies(self):
        return itertools.chain(
            (d for d, r in self.dependencies.get("compile", set()) if r),
            (d for d, r in self.dependencies.get("import", set()) if r),
            (d for d, r in self.dependencies.get("relocation", set()) if r),
            )
