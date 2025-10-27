import reflex as rx
from app.states.domain_state import DomainState
from app.components.client_modals import dialog_wrapper


def add_domain_modal() -> rx.Component:
    return dialog_wrapper(
        title="Add New Domain",
        body=rx.el.form(
            rx.el.div(
                rx.el.label("Domain Name", class_name="text-sm font-medium"),
                rx.el.input(
                    name="domain_name",
                    placeholder="e.g. example.com",
                    class_name="mt-1 w-full px-3 py-2 border rounded-md",
                ),
                class_name="mb-4",
            ),
            id="add_domain_form",
            on_submit=DomainState.add_domain,
            reset_on_submit=True,
        ),
        footer=rx.el.div(
            rx.el.button(
                "Cancel",
                on_click=DomainState.close_add_domain_modal,
                class_name="px-4 py-2 border rounded-md",
            ),
            rx.el.button(
                "Save Domain",
                type="submit",
                form="add_domain_form",
                class_name="px-4 py-2 bg-[#7BC143] text-white rounded-md hover:bg-[#6aa83a]",
            ),
            class_name="flex justify-end gap-4 pt-4",
        ),
        open_var=DomainState.show_add_domain_modal,
        on_open_change=DomainState.set_show_add_domain_modal,
    )


def edit_domain_modal() -> rx.Component:
    return rx.cond(
        DomainState.domain_to_edit,
        dialog_wrapper(
            title="Edit Domain",
            body=rx.el.form(
                rx.el.div(
                    rx.el.label("Domain Name", class_name="text-sm font-medium"),
                    rx.el.input(
                        name="domain_name",
                        default_value=DomainState.domain_to_edit["domain_name"],
                        key=DomainState.domain_to_edit["id"].to_string()
                        + "domain_name",
                        class_name="mt-1 w-full px-3 py-2 border rounded-md",
                    ),
                    class_name="mb-4",
                ),
                id="edit_domain_form",
                on_submit=DomainState.update_domain,
            ),
            footer=rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=DomainState.close_edit_domain_modal,
                    class_name="px-4 py-2 border rounded-md",
                ),
                rx.el.button(
                    "Save Changes",
                    type="submit",
                    form="edit_domain_form",
                    class_name="px-4 py-2 bg-[#7BC143] text-white rounded-md hover:bg-[#6aa83a]",
                ),
                class_name="flex justify-end gap-4 pt-4",
            ),
            open_var=DomainState.show_edit_domain_modal,
            on_open_change=DomainState.set_show_edit_domain_modal,
        ),
        rx.fragment(),
    )


def delete_domain_modal() -> rx.Component:
    return rx.cond(
        DomainState.domain_to_delete,
        dialog_wrapper(
            title="Delete Domain",
            body=rx.el.div(
                rx.el.p("Are you sure you want to delete the domain: "),
                rx.el.span(
                    DomainState.domain_to_delete["domain_name"],
                    class_name="font-semibold",
                ),
                rx.el.p("This action cannot be undone."),
            ),
            footer=rx.el.div(
                rx.el.button(
                    "Cancel",
                    on_click=DomainState.close_delete_domain_modal,
                    class_name="px-4 py-2 border rounded-md",
                ),
                rx.el.button(
                    "Delete",
                    on_click=DomainState.delete_domain,
                    class_name="px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600",
                ),
                class_name="flex justify-end gap-4 pt-4",
            ),
            open_var=DomainState.show_delete_domain_modal,
            on_open_change=DomainState.set_show_delete_domain_modal,
        ),
        rx.fragment(),
    )