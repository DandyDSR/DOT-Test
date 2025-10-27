import reflex as rx
from typing import TypedDict, Any
import datetime


class GSCData(TypedDict):
    date: str
    clicks: int
    impressions: int
    ctr: float
    position: float


class QueryData(TypedDict):
    query: str
    clicks: int
    impressions: int
    ctr: float
    position: float


class PageData(TypedDict):
    page: str
    clicks: int
    impressions: int


class AnalyticsState(rx.State):
    gsc_data: list[GSCData] = [
        {
            "date": (datetime.date.today() - datetime.timedelta(days=i)).strftime(
                "%Y-%m-%d"
            ),
            "clicks": 150 - i * 2,
            "impressions": 2500 - i * 20,
            "ctr": (150 - i * 2) / (2500 - i * 20),
            "position": 5.5 + i * 0.1,
        }
        for i in range(30)
    ]
    query_data: list[QueryData] = [
        {
            "query": "reflex framework tutorial",
            "clicks": 50,
            "impressions": 500,
            "ctr": 0.1,
            "position": 3.2,
        },
        {
            "query": "python web apps",
            "clicks": 40,
            "impressions": 600,
            "ctr": 0.067,
            "position": 4.8,
        },
        {
            "query": "how to build a dashboard in python",
            "clicks": 30,
            "impressions": 400,
            "ctr": 0.075,
            "position": 6.1,
        },
        {
            "query": "reflex vs streamlit",
            "clicks": 25,
            "impressions": 300,
            "ctr": 0.083,
            "position": 2.5,
        },
    ]
    page_data: list[PageData] = [
        {"page": "/blog/reflex-tutorial/", "clicks": 100, "impressions": 1200},
        {"page": "/docs/getting-started/", "clicks": 80, "impressions": 1000},
        {"page": "/pricing/", "clicks": 60, "impressions": 800},
    ]
    date_range: str = "30"

    @rx.var
    def filtered_gsc_data(self) -> list[GSCData]:
        days = int(self.date_range)
        return self.gsc_data[:days]

    @rx.var
    def total_clicks(self) -> int:
        return sum((d["clicks"] for d in self.filtered_gsc_data))

    @rx.var
    def total_impressions(self) -> int:
        return sum((d["impressions"] for d in self.filtered_gsc_data))

    @rx.var
    def average_ctr(self) -> float:
        if self.total_impressions == 0:
            return 0
        return self.total_clicks / self.total_impressions

    @rx.var
    def average_position(self) -> float:
        if not self.filtered_gsc_data:
            return 0
        return sum((d["position"] for d in self.filtered_gsc_data)) / len(
            self.filtered_gsc_data
        )

    @rx.event
    def on_load(self):
        pass