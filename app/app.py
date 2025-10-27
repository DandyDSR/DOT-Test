import reflex as rx
from reflex_google_auth import google_login, google_oauth_provider
from app.states.auth_state import AuthState
from app.states.client_state import ClientState, Client
from app.components.sidebar import sidebar
from app.components.client_modals import (
    add_client_modal,
    edit_client_modal,
    delete_client_modal,
)
from app.components.domain_page import domain_page
from app.components.analytics_page import analytics_page
from app.states.domain_state import DomainState
from app.states.analytics_state import AnalyticsState


def login_page() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1("dandy.", class_name="text-5xl font-bold text-[#4A9FD8] mb-4"),
            rx.el.p(
                "SEO Analysis & Optimization Tool",
                class_name="text-gray-600 mb-8 text-lg",
            ),
            google_login(),
            class_name="flex flex-col items-center justify-center text-center min-h-screen bg-gray-50",
        ),
        class_name="font-['Inter'] bg-white",
    )


def client_card(client: Client) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(client["name"], class_name="font-semibold text-lg"),
                rx.el.p(client["company"], class_name="text-sm text-gray-500"),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.p(
                    client["domain_count"].to_string() + " domains",
                    class_name="text-xs font-medium bg-[#4A9FD8]/20 text-[#4A9FD8] px-2 py-1 rounded-full",
                ),
                class_name="flex items-center",
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.div(
            rx.el.p(
                f"Last activity: {client['last_activity']}",
                class_name="text-xs text-gray-500",
            ),
            rx.el.div(
                rx.el.button(
                    "View",
                    on_click=lambda: ClientState.view_client_domains(client["id"]),
                    class_name="px-3 py-1 text-xs border rounded-md hover:bg-gray-100",
                ),
                rx.el.button(
                    "Edit",
                    on_click=lambda: ClientState.open_edit_client_modal(client),
                    class_name="px-3 py-1 text-xs border rounded-md hover:bg-gray-100",
                ),
                rx.el.button(
                    "Delete",
                    on_click=lambda: ClientState.open_delete_client_modal(client),
                    class_name="px-3 py-1 text-xs border rounded-md text-red-600 hover:bg-red-50",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between mt-4 pt-4 border-t",
        ),
        class_name="bg-white p-4 rounded-lg border shadow-sm",
    )


def dashboard() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.el.h1("Clients", class_name="text-2xl font-bold"),
                    rx.el.p(f"{ClientState.clients.length()} total clients"),
                ),
                rx.el.div(
                    rx.foreach(ClientState.clients, client_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6",
                ),
                add_client_modal(),
                edit_client_modal(),
                delete_client_modal(),
                class_name="p-6",
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full font-['Inter'] bg-gray-50",
    )


def index() -> rx.Component:
    return rx.cond(AuthState.token_is_valid, dashboard(), login_page())


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(src="https://cdn.tailwindcss.com"),
    ],
)


def wrapped_index():
    return google_oauth_provider(index())


app.add_page(
    wrapped_index,
    route="/",
    on_load=[AuthState.on_load, ClientState.on_load]
    if hasattr(ClientState, "on_load")
    else AuthState.on_load,
)


def oauth_callback():
    return rx.el.div("Processing authentication...")


app.add_page(
    domain_page,
    route="/clients/[client_id_param]/domains",
    on_load=[ClientState.on_load, DomainState.on_load],
)
app.add_page(
    oauth_callback, route="/oauth/callback", on_load=DomainState.handle_oauth_callback
)
app.add_page(
    analytics_page,
    route="/clients/[client_id_param]/domains/[domain_id]/analytics",
    on_load=[ClientState.on_load, DomainState.on_load, AnalyticsState.on_load],
)