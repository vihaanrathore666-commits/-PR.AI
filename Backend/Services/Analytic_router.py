from fastapi import APIRouter
from backend.services.analytics import StudioAnalyticsService

# Initialize an independent API sub-router segment
router = APIRouter(prefix="/api/v1/analytics", tags=["System Diagnostics Ledger"])

# Static cross-reference link hook to memory ledger services 
monitor_service = StudioAnalyticsService()

@router.get("/snapshot")
async def get_live_metrics_snapshot():
    """
    Independent endpoint pathway fetching real-time database throughput matrices, 
    average processing speeds, and design template frequencies.
    """
    # Pull dynamic monitoring configurations straight out of server cache memory
    snapshot_data = monitor_service.retrieve_dashboard_snapshot()
    return snapshot_data
