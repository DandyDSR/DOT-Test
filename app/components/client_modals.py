import reflex as rx
from app.states.client_state import ClientState


def dialog_wrapper(
    title: str,
    body: rx.Component,
    footer: rx.Component,
    open_var: rx.Var[bool],
    on_open_change,
) -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(),
        rx.radix.primitives.dialog.content(
            rx.radix.primitives.dialog.title(title),
            body,
            footer,
            rx.radix.primitives.dialog.close(
                rx.icon("x", class_name="h-4 w-4"),
                class_name="absolute top-4 right-4 rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-accent data-[state=open]:text-muted-foreground",
            ),
            style={
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "background_color": "white",
                "padding": "24px",
                "border_radius": "12px",
                "box_shadow": "0 0 10px rgba(0,0,0,0.1)",
                "max_width": "500px",
                "width": "90vw",
            },
        ),
        open=open_var,
        on_open_change=on_open_change,
    )


def add_client_modal() -> rx.Component:
    return dialog_wrapper(
        title="Add New Client",
        body=rx.el.form(
            rx.el.div(
                rx.el.label("Client Name", class_name="text-sm font-medium"),
                rx.el.input(
                    name="name",
                    placeholder="e.g. Acme Inc",
                    class_name="mt-1 w-full px-3 py-2 border rounded-md",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label("Company Name", class_name="text-sm font-medium"),
                rx.el.input(
                    name="company",
                    placeholder="e.g. Acme Corporation",
                    class_name="mt-1 w-full px-3 py-2 border rounded-md",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label("Contact Email", class_name="text-sm font-medium"),
                rx.el.input(
                    name="contact_email",
                    type="email",
                    placeholder="e.g. contact@acme.com",
                    class_name="mt-1 w-full px-3 py-2 border rounded-md",
                ),
                class_name="mb-4",
            ),
            id="add_client_form",
            on_submit=ClientState.add_client,
            reset_on_submit=True,
        ),
        footer=rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=ClientState.close_add_client_modal,
                class_name="px-4 py-2 border rounded-md",
            ),
            rx.el.button(
                "Save Client",
                type="submit",
                form="add_client_form",
                class_name="px-4 py-2 bg-[#7BC143] text-white rounded-md hover:bg-[#6aa83a]",
            ),
            class_name="flex justify-end gap-4 pt-4",
        ),
        open_var=ClientState.show_add_client_modal,
        on_open_change=ClientState.set_show_add_client_modal,
    )


def edit_client_modal() -> rx.Component:
    return rx.cond(
        ClientState.client_to_edit,
        dialog_wrapper(
            title="Edit Client",
            body=rx.el.form(
                rx.el.div(
                    rx.el.label("Client Name", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="name",
                        default_value=ClientState.client_to_edit["name"],
                        key=ClientState.client_to_edit["id"].to_string() + "name",
                        class_name="mt-1 w-full px-3 py-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Company Name", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="company",
                        default_value=ClientState.client_to_edit["company"],
                        key=ClientState.client_to_edit["id"].to_string() + "company",
                        class_name="mt-1 w-full px-3 py-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Contact Email", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="contact_email",
                        type="email",
                        default_value=ClientState.client_to_edit["contact_email"],
                        key=ClientState.client_to_edit["id"].to_string() + "email",
                        class_name="mt-1 w-full px-3 py-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                id="edit_client_form",
                on_submit=ClientState.update_client,
            ),
            footer=rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=ClientState.close_edit_client_modal,
                    class_name="px-4 py-2 border rounded-md",
                ),
                rx.el.button(
                    "Save Changes",
                    type="submit",
                    form="edit_client_form",
                    class_name="px-4 py-2 bg-[#7BC143] text-white rounded-md hover:bg-[#6aa83a]",
                ),
                class_name="flex justify-end gap-4 pt-4",
            ),
            open_var=ClientState.show_edit_client_modal,
            on_open_change=ClientState.set_show_edit_client_modal,
        ),
        rx.fragment(),
    )


def delete_client_modal() -> rx.Component:
    return rx.cond(
        ClientState.client_to_delete,
        dialog_wrapper(
            title="Delete Client",
            body=rx.el.div(
                rx.el.p("Are you sure you want to delete the client: "),
                rx.el.span(
                    ClientState.client_to_delete["name"], class_name="font-semibold"
                ),
                rx.el.p("This action cannot be undone."),
            ),
            footer=rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=ClientState.close_delete_client_modal,
                    class_name="px-4 py-2 border rounded-md",
                ),
                rx.el.button(
                    "Delete",
                    on_click=ClientState.delete_client,
                    class_name="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600",
                ),
                class_name="flex justify-end gap-4 pt-4",
            ),
            open_var=ClientState.show_delete_client_modal,
            on_open_change=ClientState.set_show_delete_client_modal,
        ),
        rx.fragment(),
    )