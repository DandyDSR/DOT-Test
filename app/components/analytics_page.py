import reflex as rx
from app.states.client_state import ClientState
from app.states.domain_state import DomainState, Domain
from app.states.analytics_state import AnalyticsState
from app.components.sidebar import sidebar

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "border_color": "#E8E8E8",
        "border_radius": "0.75rem",
    },
    "item_style": {},
    "label_style": {"color": "black"},
    "separator": "",
}


def metric_card(title: str, value: rx.Var[str], trend: str) -> rx.Component:
    return rx.el.div(
        rx.el.h3(title, class_name="text-sm font-medium text-gray-500"),
        rx.el.p(value, class_name="text-3xl font-bold"),
        rx.el.p(trend, class_name="text-sm text-green-500"),
        class_name="bg-white p-6 rounded-lg border shadow-sm",
    )


def analytics_chart() -> rx.Component:
    return rx.recharts.area_chart(
        rx.recharts.cartesian_grid(
            horizontal=True, vertical=False, stroke_dasharray="3 3"
        ),
        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
        rx.recharts.x_axis(
            data_key="date", tick_line=False, axis_line=False, tick_margin=10
        ),
        rx.recharts.y_axis(
            tick_line=False, axis_line=False, tick_margin=10, domain=["auto", "auto"]
        ),
        rx.recharts.area(
            data_key="clicks",
            type_="natural",
            fill="#4A9FD8",
            stroke="#4A9FD8",
            stack_id="1",
        ),
        rx.recharts.area(
            data_key="impressions",
            type_="natural",
            fill="#7BC143",
            stroke="#7BC143",
            stack_id="2",
        ),
        data=AnalyticsState.filtered_gsc_data,
        height=400,
        width="100%",
        class_name="[&_.recharts-tooltip-cursor]:fill-zinc-200/50",
    )


def data_table(columns: list[dict], data: rx.Var[list[dict]]) -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.foreach(
                        columns,
                        lambda col: rx.el.th(
                            col["header"], class_name="text-left font-semibold p-4"
                        ),
                    )
                ),
                class_name="bg-gray-50 border-b",
            ),
            rx.el.tbody(
                rx.foreach(
                    data,
                    lambda row: rx.el.tr(
                        rx.foreach(
                            columns,
                            lambda col: rx.el.td(
                                row[col["accessor"]].to_string(), class_name="p-4"
                            ),
                        ),
                        class_name="border-b",
                    ),
                )
            ),
            class_name="w-full text-sm",
        ),
        class_name="bg-white rounded-lg border shadow-sm overflow-hidden",
    )


def analytics_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "SEO Analytics Dashboard", class_name="text-2xl font-bold"
                    ),
                    rx.el.p(DomainState.domain_to_connect.to_string()),
                ),
                rx.el.div(
                    rx.el.select(
                        rx.el.option("Last 7 Days", value="7"),
                        rx.el.option("Last 30 Days", value="30"),
                        rx.el.option("Last 90 Days", value="90"),
                        value=AnalyticsState.date_range,
                        on_change=AnalyticsState.set_date_range,
                        class_name="px-3 py-2 border rounded-md",
                    ),
                    class_name="flex justify-end mb-6",
                ),
                rx.el.div(
                    metric_card(
                        "Total Clicks",
                        AnalyticsState.total_clicks.to_string(),
                        "+12.5%",
                    ),
                    metric_card(
                        "Total Impressions",
                        AnalyticsState.total_impressions.to_string(),
                        "+20.1%",
                    ),
                    metric_card(
                        "Average CTR",
                        (AnalyticsState.average_ctr * 100).to_string() + "%",
                        "+2.5%",
                    ),
                    metric_card(
                        "Average Position",
                        AnalyticsState.average_position.to_string(),
                        "-0.5",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6",
                ),
                rx.el.div(
                    analytics_chart(),
                    class_name="bg-white p-6 rounded-lg border shadow-sm mb-6",
                ),
                rx.el.h2("Query Performance", class_name="text-xl font-bold mb-4"),
                data_table(
                    columns=[
                        {"header": "Query", "accessor": "query"},
                        {"header": "Clicks", "accessor": "clicks"},
                        {"header": "Impressions", "accessor": "impressions"},
                        {"header": "CTR", "accessor": "ctr"},
                        {"header": "Position", "accessor": "position"},
                    ],
                    data=AnalyticsState.query_data,
                ),
                rx.el.h2("Page Performance", class_name="text-xl font-bold my-4"),
                data_table(
                    columns=[
                        {"header": "Page", "accessor": "page"},
                        {"header": "Clicks", "accessor": "clicks"},
                        {"header": "Impressions", "accessor": "impressions"},
                    ],
                    data=AnalyticsState.page_data,
                ),
                class_name="p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full font-['Inter'] bg-gray-50",
    )