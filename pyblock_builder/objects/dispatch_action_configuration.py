import sys
if sys.version_info >= (3, 11):
    from typing import Self
else:
    from typing_extensions import Self

class DispatchActionConfig:
    """
    A Python class representing a Dispatch action configuration from the Slack BlockKit UI framework
    """
    def __init__(self):
        self._trigger_actions_on = []
        self.json = {
            "trigger_actions_on": self._trigger_actions_on
        }

    def set_triggers(self, *triggers) -> Self:
        """
        Sets the interaction types that you would like to receive a block_actions payload for
        :param triggers: Must be one or both of "on_enter_pressed" or "on_character_entered"; preface with * if passing in a list
        :return: self
        """
        for trigger in triggers:
            self._trigger_actions_on.append(trigger)
        self.json["trigger_actions_on"] = self._trigger_actions_on
        return self
