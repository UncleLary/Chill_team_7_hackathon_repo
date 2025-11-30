from typing import Dict, Any

from fastapi import FastAPI, APIRouter, Depends, HTTPException, status

from core.llm import AgentWorkflowEngine, get_agent_workflow_engine
from schemas.llm import LLMRequest

def get_llm_router() -> APIRouter:
    """Generate a router for LLM workflow operations."""
    router = APIRouter()

    @router.post(
        "/run",
        response_model=Dict[str, Any],
        name="llm:run_flow",
        status_code=status.HTTP_200_OK,
        responses={
            status.HTTP_500_INTERNAL_SERVER_ERROR: {
                "description": "Internal server error during workflow execution.",
            },
        },
    )
    async def run_flow(
        request: LLMRequest,
        engine: AgentWorkflowEngine = Depends(get_agent_workflow_engine),
    ):
        """
        Execute the LLM agent workflow.
        """
        try:
            return await engine.run_flow(request.template_name, request.arguments)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error executing workflow: {str(e)}"
            )

    return router

def include_routers(app: FastAPI):
    app.include_router(get_llm_router(), prefix="/llm", tags=["llm"])
