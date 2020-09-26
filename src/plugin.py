from LSP.plugin import AbstractPlugin
from LSP.plugin.core.typing import Optional, Any, Tuple, List, Dict, Mapping
import sublime_plugin
import sublime

# TODO: Expose in public API
from LSP.plugin.core.url import filename_to_uri
from LSP.plugin.core.promise import Promise


def _deeper_dict(d: Dict[str, Any], key: str) -> Dict[str, Any]:
    if key not in d:
        d[key] = {}
    return d[key]


class SonarLint(AbstractPlugin):
    @classmethod
    def name(cls) -> str:
        return cls.__name__

    @classmethod
    def additional_variables(cls) -> Optional[Dict[str, str]]:
        return {
            "packages_uri": filename_to_uri(sublime.packages_path()),
            "name": "LSP-{}".format(cls.name())
        }

    def on_pre_server_command(self, command: Mapping[str, Any]) -> Optional[Promise]:
        session = self.weaksession()
        if not session:
            return Promise.resolve()
        if command["command"] == "SonarLint.OpenRuleDesc":
            view = session.window.active_view()
            view.show_popup("<h1>{}</h1><h2>{}</h2>{}".format(*command["arguments"]))
            return Promise.resolve()
        if command["command"] == "SonarLint.DeactivateRule":
            data = session.window.project_data()
            root = data
            data = _deeper_dict(data, "settings")
            data = _deeper_dict(data, "LSP")
            data = _deeper_dict(data, "LSP-SonarLint")
            data = _deeper_dict(data, "settings")
            data.setdefault("sonarlint.excludedRules", []).append(command["arguments"][0])
            session.window.set_project_data(root)
            return Promise.resolve()
