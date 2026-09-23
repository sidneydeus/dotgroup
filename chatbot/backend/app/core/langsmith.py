import os
from langsmith import Client
from langsmith.run_trees import RunTree
from app.core.config import get_settings

_langsmith_client: Client | None = None


def init_langsmith() -> Client | None:
    """Initialize LangSmith client if configured."""
    global _langsmith_client

    settings = get_settings()

    if not settings.langsmith_api_key:
        return None

    if _langsmith_client is None:
        os.environ["LANGSMITH_API_KEY"] = settings.langsmith_api_key
        os.environ["LANGSMITH_PROJECT"] = settings.langsmith_project
        os.environ["LANGSMITH_ENDPOINT"] = settings.langsmith_endpoint
        if settings.langsmith_tracing:
            os.environ["LANGSMITH_TRACING"] = "true"
        _langsmith_client = Client(
            api_key=settings.langsmith_api_key,
            api_url=settings.langsmith_endpoint,
        )

    return _langsmith_client


def get_langsmith_client() -> Client | None:
    """Get the LangSmith client, initializing if needed."""
    global _langsmith_client
    if _langsmith_client is None:
        init_langsmith()
    return _langsmith_client


def create_run_tree(
    name: str,
    inputs: dict,
    run_type: str = "chain",
    session_id: str | None = None,
) -> RunTree | None:
    """Create a LangSmith run tree for tracing."""
    client = get_langsmith_client()
    if client is None:
        return None

    run_tree = RunTree(
        name=name,
        inputs=inputs,
        run_type=run_type,
        session_id=session_id,
    )
    run_tree.post()
    return run_tree


def end_run_tree(run_tree: RunTree | None, outputs: dict | None = None, error: str | None = None) -> None:
    """End a LangSmith run tree."""
    if run_tree is None:
        return

    if error:
        run_tree.end(error=error)
    else:
        run_tree.end(outputs=outputs or {})
    run_tree.post()