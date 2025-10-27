import reflex as rx
from app.states.client_state import ClientState
from app.states.domain_state import DomainState, Domain
from app.components.sidebar import sidebar
from app.components.domain_modals import (
    add_domain_modal,
    edit_domain_modal,
    delete_domain_modal,
)


def connection_toggle(domain: Domain, service: str) -> rx.Component:
    is_connected = rx.cond(
        service == "gsc", domain["gsc_connected"], domain["ga4_connected"]
    )
    label = rx.cond(service == "gsc", "GSC Connected", "GA4 Connected")
    return rx.el.div(
        rx.el.label(
            rx.el.input(
                type="checkbox",
                checked=is_connected,
                on_change=lambda _: DomainState.initiate_connection(domain, service),
                class_name="sr-only peer",
                disabled=is_connected,
            ),
            rx.el.div(
                class_name="w-11 h-6 bg-gray-200 rounded-full peer peer-focus:ring-4 peer-focus:ring-blue-300 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-600"
            ),
            rx.el.span(label, class_name="ml-3 text-sm font-medium text-gray-900"),
            class_name="relative inline-flex items-center cursor-pointer",
        ),
        class_name="flex items-center",
    )


def domain_card(domain: Domain) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(domain["domain_name"], class_name="font-semibold text-lg"),
            rx.el.div(
                connection_toggle(domain, "gsc"),
                connection_toggle(domain, "ga4"),
                class_name="flex items-center gap-6 mt-4",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.button(
                "View Analytics",
                on_click=lambda: DomainState.view_domain_analytics(domain["id"]),
                class_name="px-3 py-1 text-xs bg-[#4A9FD8] text-white rounded-md hover:bg-[#3b82f6]",
            ),
            rx.el.button(
                "Edit",
                on_click=lambda: DomainState.open_edit_domain_modal(domain),
                class_name="px-3 py-1 text-xs border rounded-md hover:bg-gray-100",
            ),
            rx.el.button(
                "Delete",
                on_click=lambda: DomainState.open_delete_domain_modal(domain),
                class_name="px-3 py-1 text-xs border rounded-md text-red-600 hover:bg-red-50",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="bg-white p-4 rounded-lg border shadow-sm flex items-center justify-between",
    )


def domain_page() -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.cond(
                ClientState.selected_client,
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            ClientState.selected_client["name"].to_string()
                            + "'s Domains",
                            class_name="text-2xl font-bold",
                        ),
                        rx.el.p(
                            f"{DomainState.selected_client_domains.length()} total domains"
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("plus", class_name="mr-2 h-4 w-4"),
                            "Add Domain",
                            on_click=DomainState.open_add_domain_modal,
                            class_name="flex items-center bg-[#7BC143] text-white px-4 py-2 rounded-lg hover:bg-[#6aa83a]",
                        ),
                        class_name="flex justify-end mb-6",
                    ),
                    rx.el.div(
                        rx.foreach(DomainState.selected_client_domains, domain_card),
                        class_name="grid grid-cols-1 gap-6",
                    ),
                    add_domain_modal(),
                    edit_domain_modal(),
                    delete_domain_modal(),
                    class_name="p-6",
                ),
                rx.el.div("Loading client..."),
            ),
            class_name="flex-1",
        ),
        class_name="flex min-h-screen w-full font-['Inter'] bg-gray-50",
    )