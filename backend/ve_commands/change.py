import json
import os

from backend.commands.commandLine import line
from backend.commands.basedCommand import based
from backend.commands.delete import delete
from based.based_values import values

class change(based):

    def cast(self, cl: line) -> list[str]:
        self.check(cl)
        self.__init__(self.padding, cl)
        if (self.get(0) == "change" and (self.get(1) not in [None, "", " "])):
            name = ""
            if (self.get(1) == "l"):
                name = f"{values().get_base_stack_for_last_level_created_name()}.json"
            else:
                name = f"{self.get(1)}.json"
            if (name in os.listdir(f"{values().get_base_directory()}/Terminal/Levels")):
                with open(f"{values().get_base_directory()}/Terminal/Levels/{name}", "r") as file:
                    data = json.load(file)
                data = dict(data)
                with open(f"backend/preFiles/app/activate.json", "w+") as wr_f:
                    json.dump(data, wr_f)
                del data
                delete().other_cast()
                return ["Success changed to last created level!"]
            else:
                return ["This level is not be found!"]
        elif (self.get(0) == "change" and (self.get(1) in [None, " ", ""])):
            f = open(f"backend/preFiles/app/change_help_command", "r")
            file = f.readlines()
            f.close()
            for i in range(len(file)):
                if ("\n" in file[i]):
                    file[i] = file[i].replace("\n", "")
            return file
        return []
