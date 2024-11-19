from typing import TypeVar

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from services.agents.analyst import DataAnalystAgent
from services.agents.developer import DeveloperAgent
from services.agents.planner import PlannerAgent
from services.agents.supervisor import SupervisorAgent
from services.agents.types import AgentContext

T = TypeVar("T")


def create_agent_graph(
    supervisor: SupervisorAgent,
    planner: PlannerAgent,
    analyst: DataAnalystAgent,
    developer: DeveloperAgent,
) -> CompiledStateGraph:
    """Create the agent workflow graph."""

    workflow = StateGraph(AgentContext)

    # Add nodes for each agent
    workflow.add_node("supervisor", supervisor.agent_executor)
    workflow.add_node("planner", lambda context: planner.execute(context))
    workflow.add_node("analyst", lambda context: analyst.execute(context))
    workflow.add_node("developer", lambda context: developer.execute(context))

    # Define the edges and conditions
    workflow.add_edge("planner", "supervisor")
    workflow.add_edge("analyst", "supervisor")
    workflow.add_edge("developer", "supervisor")
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next"],
        {
            "planner": "planner",
            "analyst": "analyst",
            "developer": "developer",
            "FINISH": END,
        },
    )

    workflow.add_edge(START, "supervisor")

    # Compile the graph
    return workflow.compile()
