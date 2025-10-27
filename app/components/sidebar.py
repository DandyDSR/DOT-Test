import reflex as rx
from app.states.auth_state import AuthState
from app.states.client_state import ClientState, Client


def nav_item(client: Client) -> rx.Component:
    return rx.el.a(
        rx.image(
            src=f"https://api.dicebear.com/9.x/initials/svg?seed={client['name']}",
            class_name="h-8 w-8 rounded-full",
        ),
        rx.el.span(client["name"], class_name="truncate"),
        on_click=lambda: ClientState.set_selected_client_id(client["id"]),
        class_name=rx.cond(
            ClientState.selected_client_id == client["id"],
            "flex items-center gap-3 rounded-lg bg-[#4A9FD8]/20 px-3 py-2 text-[#4A9FD8] transition-all hover:text-[#4A9FD8] cursor-pointer",
            "flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900 cursor-pointer",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.el.h1("dandy.", class_name="text-2xl font-bold text-[#4A9FD8]"),
                    href="/",
                    class_name="flex items-center gap-2 font-semibold",
                ),
                rx.el.div(
                    rx.el.p(
                        AuthState.tokeninfo.get("given_name", ""),
                        class_name="font-semibold",
                    ),
                    rx.el.p(
                        AuthState.tokeninfo.get("email", ""),
                        class_name="text-xs text-gray-500",
                    ),
                    class_name="text-right",
                ),
                class_name="flex items-center justify-between border-b pb-4",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.foreach(ClientState.clients, nav_item),
                    class_name="grid items-start gap-1",
                ),
                class_name="grid items-start font-medium",
            ),
            class_name="flex-1 overflow-auto py-4",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("circle_plus", class_name="h-4 w-4 mr-2"),
                "Add Client",
                on_click=ClientState.open_add_client_modal,
                class_name="flex items-center justify-center w-full bg-[#7BC143] text-white rounded-lg px-4 py-2 hover:bg-[#6aa83a] transition-colors",
            ),
            rx.el.button(
                rx.icon("log-out", class_name="h-4 w-4 mr-2"),
                "Logout",
                on_click=AuthState.logout,
                class_name="flex items-center justify-center w-full bg-gray-200 text-gray-700 rounded-lg px-4 py-2 mt-2 hover:bg-gray-300 transition-colors",
            ),
            class_name="mt-auto p-4 border-t",
        ),
        class_name="hidden border-r bg-gray-100/40 md:flex md:flex-col min-h-screen w-72",
    )