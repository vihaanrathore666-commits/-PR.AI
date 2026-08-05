import time
from typing import Dict, Any

class StudioAnalyticsService:
    """
    Self-contained tracking engine monitoring background extraction metrics,
    4K master output scale history, and premium affiliate campaign click actions.
    """
    def __init__(self):
        # Operational ledger held safely within internal cluster memory structures
        self._global_ledger = {
            "total_render_count": 0,
            "style_metrics": {
                "zara": 0,
                "apple": 0,
                "dark_luxury": 0,
                "streetwear": 0
            },
            "resolution_metrics": {
                "instagram_feed": 0,
                "instagram_story": 0,
                "4k_master": 0
            },
            "accumulated_bytes_processed": 0,
            "performance_latency_history": []
        }

    def log_generation_event(self, style: str, resolution: str, file_size_bytes: int, compute_time_ms: float) -> None:
        """
        Registers an isolated metric update entry without changing external pipeline flows.
        """
        self._global_ledger["total_render_count"] += 1
        
        # Track style choice volumes
        if style in self._global_ledger["style_metrics"]:
            self._global_ledger["style_metrics"][style] += 1
            
        # Track canvas scaling distribution matrices
        if resolution in self._global_ledger["resolution_metrics"]:
            self._global_ledger["resolution_metrics"][resolution] += 1
            
        # Compile processed file bandwidth footprints
        self._global_ledger["accumulated_bytes_processed"] += file_size_bytes
        
        # Track rendering engine processing velocities
        self._global_ledger["performance_latency_history"].append(compute_time_ms)
        if len(self._global_ledger["performance_latency_history"]) > 100:
            self._global_ledger["performance_latency_history"].pop(0)

    def retrieve_dashboard_snapshot(self) -> Dict[str, Any]:
        """
        Compiles structural diagnostic summary sheets to render on the mobile user interface.
        """
        history = self._global_ledger["performance_latency_history"]
        avg_speed = sum(history) / len(history) if history else 0.0
        
        # Convert total processing load into readable Megabytes for mobile viewing
        mb_processed = round(self._global_ledger["accumulated_bytes_processed"] / (1024 * 1024), 2)
        
        return {
            "studio_status": "optimal",
            "lifetime_renders": self._global_ledger["total_render_count"],
            "data_throughput_mb": mb_processed,
            "average_pipeline_speed_ms": round(avg_speed, 2),
            "popular_archetype": max(self._global_ledger["style_metrics"], key=self._global_ledger["style_metrics"].get),
            "distribution_summary": {
                "styles": self._global_ledger["style_metrics"],
                "formats": self._global_ledger["resolution_metrics"]
            }
        }
