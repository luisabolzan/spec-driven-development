from __future__ import annotations

from typing import Iterable


class ExperimentListView:
    def __init__(self):
        self.items: list[dict] = []

    def set_items(self, experiments: Iterable[dict]) -> None:
        self.items = list(experiments)

    def render(self) -> list[str]:
        return [f"{item['id']} - {item['name']}" for item in self.items]
