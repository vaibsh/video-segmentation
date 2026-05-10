from dataclasses import dataclass
import config.config as cfg

@dataclass
class RuntimeConfig:
    PEAK_DISTANCE: int
    SEARCH_RADIUS: int
    SEMANTIC_CONTEXT: int
    PEAK_CONTEXT: int


def build_runtime_config(fps: float) -> RuntimeConfig:
    return RuntimeConfig(
        PEAK_DISTANCE=int(cfg.PEAK_DISTANCE_FACTOR * fps),

        SEARCH_RADIUS=int(cfg.SEARCH_RADIUS_FACTOR * fps),

        SEMANTIC_CONTEXT=int(cfg.SEMANTIC_CONTEXT_FACTOR * fps),

        PEAK_CONTEXT=max(
            3,
            int(cfg.PEAK_CONTEXT_FACTOR * fps)
        ),
    )