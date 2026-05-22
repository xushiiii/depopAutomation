"""Randomized delays between automation steps to mimic human pacing."""
import random
import time

# Tune these if listings still feel too fast or too slow.
SHORT_MIN, SHORT_MAX = 0.4, 1.0
MEDIUM_MIN, MEDIUM_MAX = 0.9, 2.2
LONG_MIN, LONG_MAX = 1.8, 3.8
THINK_CHANCE = 0.2  # occasional longer pause between sections


def human_pause(min_s: float, max_s: float) -> None:
    time.sleep(random.uniform(min_s, max_s))


def pause_short() -> None:
    human_pause(SHORT_MIN, SHORT_MAX)


def pause_medium() -> None:
    human_pause(MEDIUM_MIN, MEDIUM_MAX)


def pause_long() -> None:
    human_pause(LONG_MIN, LONG_MAX)


def pause_between_steps() -> None:
    """Default gap between form fields / actions."""
    pause_short()
    if random.random() < THINK_CHANCE:
        pause_long()


def pause_between_sections() -> None:
    """Gap between logical groups (category block, shipping, etc.)."""
    pause_medium()
    if random.random() < THINK_CHANCE:
        pause_long()
