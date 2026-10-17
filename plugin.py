from __future__ import annotations

from LSP.plugin import command_handler
from LSP.plugin import css
from LSP.plugin import filename_to_uri
from LSP.plugin import LspPlugin
from LSP.plugin import OnPreStartContext
from LSP.plugin import PackagedTask
from LSP.plugin import Promise
from LSP.plugin import Session
from typing import Any
from typing import Callable
import html.parser
import mdpopups
import sublime


def _deeper_dict(d: dict[str, Any], key: str) -> dict[str, Any]:
    if key not in d:
        d[key] = {}
    return d[key]


class HTMLParser(html.parser.HTMLParser):
    """
    Workaround for minihtml not understanding <code> and <pre> tags.
    """

    def __init__(self, language_id: str) -> None:
        super().__init__()
        self.language_id = language_id
        self.result = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "pre":
            self.result += "```{}".format(self.language_id)
        elif tag == "code":
            self.result += "`"
        elif tag == "p":
            if self.result:
                self.result += "\n"
        else:
            attributes = ""
            for name, value in attrs:
                attributes += ' {}="{}"'.format(name, value)
            self.result += "<{}{}>".format(tag, attributes)

    def handle_endtag(self, tag: str) -> None:
        if tag == "pre":
            self.result += "```\n"
        elif tag == "code":
            self.result += "`"
        elif tag == "p":
            self.result += "\n"
        else:
            self.result += "</{}>".format(tag)

    def handle_data(self, data: str) -> None:
        self.result += data


class SonarLint(LspPlugin):
    @classmethod
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        context.variables.update({
            "packages_uri": filename_to_uri(sublime.packages_path()),
            "name": cls.name
        })

    @command_handler("SonarLint.OpenRuleDesc")
    def on_open_rule_description(self, arguments: list[Any] | None) -> Promise[None]:
        session = self.weaksession()
        if session and arguments:
            try:
                self._handle_open_rule_description(session, session.window, arguments)
            except Exception:
                pass
        return Promise.resolve(None)

    @command_handler("SonarLint.DeactivateRule")
    def on_deactivate_rule(self, arguments: list[Any] | None) -> Promise[None]:
        session = self.weaksession()
        if not session or not arguments:
            return Promise.resolve(None)
        task: PackagedTask[None] = Promise.packaged_task()
        promise, resolve = task
        self._handle_deactivate_rule(session.window, arguments, lambda: resolve(None))
        return promise

    def _handle_open_rule_description(self, session: Session, window: sublime.Window, args: list[str]) -> None:
        view = window.active_view()
        if not view:
            return
        file_name = view.file_name()
        language_id = "text"
        if file_name:
            uri = filename_to_uri(file_name)
            sb = session.get_session_buffer_for_uri_async(uri)
            if sb:
                language_id = sb.get_language_id() or "txt"
        parser = HTMLParser(language_id)
        parser.feed("<p><i>{}</i></p>{}".format(args[1], args[2]))
        mdpopups.new_html_sheet(
            window=window,
            name=args[0],
            contents=parser.result,
            css=css().sheets,
            wrapper_class=css().sheets_classname,
            flags=sublime.ADD_TO_SELECTION | sublime.SEMI_TRANSIENT)

    def _handle_deactivate_rule(self, window: sublime.Window, args: list[str], done: Callable[[], None]) -> None:
        data = window.project_data()
        if data is None or not isinstance(data, dict):
            done()
            return
        root = data
        rule = args[0]
        data = _deeper_dict(data, "settings")
        data = _deeper_dict(data, "LSP")
        data = _deeper_dict(data, self.name)
        data = _deeper_dict(data, "settings")
        data = _deeper_dict(data, "sonarlint")
        data = _deeper_dict(data, "rules")
        data[rule] = {"level": "off"}
        window.set_project_data(root)

        def report_to_user() -> None:
            fmt = "".join((
                'The rule "{}" was added to the excluded list for SonarLint in your window project data. ',
                'If your window is maintained by a sublime project, the server should be restarted automatically. ',
                'Otherwise, you need to restart the server manually.'
            ))
            sublime.message_dialog(fmt.format(rule))
            done()

        sublime.set_timeout(report_to_user)


def plugin_loaded() -> None:
    SonarLint.register()


def plugin_unloaded() -> None:
    SonarLint.unregister()
