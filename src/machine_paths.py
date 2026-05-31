"""Desktop vs laptop file paths. Toggle via the app UI (defaults to desktop)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

Machine = Literal["desktop", "laptop"]

DEPOP_CSV_FILENAME = "depop_drafts.csv"


@dataclass(frozen=True)
class MachinePaths:
    edge_user_data_dir: str
    edge_profile_dir: str
    edge_driver_path: str
    service_account_file: str
    depop_csv_path: Path
    depop_earnings_log_dir: Path
    ebay_earnings_log_dir: Path
    pirateship_earnings_log_dir: Path
    ebay_listings_dir: Path


_DESKTOP = MachinePaths(
    edge_user_data_dir=r"C:\Users\Taylor Xu\AppData\Local\Microsoft\Edge\User Data",
    edge_profile_dir="Default",
    edge_driver_path=r"C:\Users\Taylor Xu\Downloads\edgedriver_win64 (2)\msedgedriver.exe",
    service_account_file=r"C:\Users\Taylor Xu\Downloads\resellingautomation-1044349da8d8.json",
    depop_csv_path=Path(r"C:\Users\Taylor Xu\Downloads") / DEPOP_CSV_FILENAME,
    depop_earnings_log_dir=Path(r"C:\Users\Taylor Xu\OneDrive\Desktop\depop_earnings"),
    ebay_earnings_log_dir=Path(r"C:\Users\Taylor Xu\OneDrive\Desktop\ebay_earnings"),
    pirateship_earnings_log_dir=Path(r"C:\Users\Taylor Xu\OneDrive\Desktop\pirateship_earnings"),
    ebay_listings_dir=Path(r"C:\Users\Taylor Xu\Downloads\ebay_listings"),
)

_LAPTOP = MachinePaths(
    edge_user_data_dir=r"C:\Users\taylo\AppData\Local\Microsoft\Edge\User Data",
    edge_profile_dir="Default",
    edge_driver_path=r"C:\Users\taylo\Downloads\edgedriver_win64 (1)\msedgedriver.exe",
    service_account_file=r"C:\Users\taylo\Downloads\resellingautomation-7a1c1c833f65.json",
    depop_csv_path=Path(r"C:\Users\taylo\Downloads") / DEPOP_CSV_FILENAME,
    depop_earnings_log_dir=Path(r"C:\Users\taylo\OneDrive\Desktop\depop_earnings"),
    ebay_earnings_log_dir=Path(r"C:\Users\taylo\OneDrive\Desktop\ebay_earnings"),
    pirateship_earnings_log_dir=Path(r"C:\Users\taylo\OneDrive\Desktop\pirateship_earnings"),
    ebay_listings_dir=Path(r"C:\Users\taylo\Downloads\ebay_listings"),
)

_PATHS = {"desktop": _DESKTOP, "laptop": _LAPTOP}
_machine: Machine = "desktop"


def get_machine() -> Machine:
    return _machine


def set_machine(machine: str) -> None:
    global _machine
    if machine not in _PATHS:
        raise ValueError(f"Unknown machine: {machine!r}")
    _machine = machine  # type: ignore[assignment]


def get_paths() -> MachinePaths:
    return _PATHS[_machine]
