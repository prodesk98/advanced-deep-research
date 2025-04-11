from typing import Optional, Any
from uuid import UUID

from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.callbacks import BaseCallbackHandler
from streamlit.delta_generator import DeltaGenerator

from loggings import logger


class AgentCallbackHandler(BaseCallbackHandler):
    def __init__(self, ui: Optional[DeltaGenerator] = None):
        self._ui = ui
        self.actions: dict[str, str] = {}

    def on_agent_action(
        self,
        action: AgentAction,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        self.actions[run_id.hex] = action.tool
        logger(message=f"⚙️ Agent action: {action.tool} with input: {action.tool_input}", level="info", ui=self._ui)


    def on_agent_finish(
        self,
        finish: AgentFinish,
        *,
        run_id: UUID,
        parent_run_id: Optional[UUID] = None,
        **kwargs: Any,
    ) -> Any:
        logger(message=f"✅ Agent Finished", level="info", ui=self._ui)
