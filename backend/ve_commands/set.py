
from backend.commands.commandLine import line
from backend.commands.basedCommand import based

from based.langist import language, LanguageException

class set(based):

    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        super().__init__(self.padding, cl)
        if ((len(cl.command) in [3, 4])
            and self.get(0) == "set"
            and self.get(1) in ["lan", "language", "lang"]):
            try:
                language().set_lang(self.get(2))
                return language().__getitem__("success_setting_language_message")
            except LanguageException:
                return language().__getitem__("setting_language_error_message")
        elif ((len(cl.command) == 1)
            or (len(cl.command)) == 2 and (self.get(1) in [None, "", " "])):
            return language().__getitem__("set_command")
        else:
            return language().__getitem__("cant_applied_command")
