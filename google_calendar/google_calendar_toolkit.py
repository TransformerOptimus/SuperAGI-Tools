from abc import ABC
from superagi.tools.base_tool import BaseToolkit, BaseTool, ToolConfiguration
from typing import Type, List
from create_calendar_event import CreateEventCalendarTool
from delete_calendar_event import DeleteCalendarEventTool
from list_calendar_events import ListCalendarEventsTool
from event_details_calendar import EventDetailsCalendarTool
from superagi.types.key_type import ToolConfigKeyType

class GoogleCalendarToolKit(BaseToolkit, ABC):
    name: str = "Google Calendar Toolkit"
    description: str = "Google Calendar Tool kit contains all tools related to Google Calendar"

    def get_tools(self) -> List[BaseTool]:
        return [CreateEventCalendarTool(), DeleteCalendarEventTool(), ListCalendarEventsTool(), EventDetailsCalendarTool()]

    def get_env_keys(self) -> List[ToolConfiguration]:
        return [
            ToolConfiguration(key="GOOGLE_CLIENT_ID", key_type=ToolConfigKeyType.STRING, is_required= True, is_secret = False),
            ToolConfiguration(key="GOOGLE_CLIENT_SECRET", key_type=ToolConfigKeyType.STRING, is_required= True, is_secret= True)
        ]
    