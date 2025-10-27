import reflex as rx
from typing import TypedDict
import datetime
import logging


class Client(TypedDict):
    id: int
    name: str
    company: str
    contact_email: str
    domain_count: int
    last_activity: str


class ClientState(rx.State):
    clients: list[Client] = [
        {
            "id": 1,
            "name": "Reflex",
            "company": "Reflex Inc.",
            "contact_email": "user@reflex.dev",
            "domain_count": 2,
            "last_activity": "2024-05-20T10:00:00Z",
        },
        {
            "id": 2,
            "name": "Dandy Marketing",
            "company": "Dandy Co.",
            "contact_email": "hello@dandy.co.uk",
            "domain_count": 5,
            "last_activity": "2024-05-22T14:30:00Z",
        },
    ]
    show_add_client_modal: bool = False
    show_edit_client_modal: bool = False
    show_delete_client_modal: bool = False
    client_to_edit: Client | None = None
    client_to_delete: Client | None = None
    selected_client_id: int = 1

    @rx.var
    def selected_client(self) -> Client | None:
        for client in self.clients:
            if client["id"] == self.selected_client_id:
                return client
        return self.clients[0] if self.clients else None

    @rx.event
    def set_selected_client_id(self, client_id: int):
        self.selected_client_id = client_id

    @rx.event
    def open_add_client_modal(self):
        self.show_add_client_modal = True

    @rx.event
    def close_add_client_modal(self):
        self.show_add_client_modal = False

    @rx.event
    def add_client(self, form_data: dict):
        new_id = max([c["id"] for c in self.clients]) + 1 if self.clients else 1
        new_client: Client = {
            "id": new_id,
            "name": form_data["name"],
            "company": form_data["company"],
            "contact_email": form_data["contact_email"],
            "domain_count": 0,
            "last_activity": datetime.datetime.now().isoformat() + "Z",
        }
        self.clients.append(new_client)
        self.show_add_client_modal = False

    @rx.event
    def open_edit_client_modal(self, client: Client):
        self.client_to_edit = client
        self.show_edit_client_modal = True

    @rx.event
    def close_edit_client_modal(self):
        self.show_edit_client_modal = False
        self.client_to_edit = None

    @rx.event
    def update_client(self, form_data: dict):
        if self.client_to_edit:
            client_id_to_update = self.client_to_edit["id"]
            self.clients = [
                {
                    **c,
                    "name": form_data["name"],
                    "company": form_data["company"],
                    "contact_email": form_data["contact_email"],
                }
                if c["id"] == client_id_to_update
                else c
                for c in self.clients
            ]
            self.close_edit_client_modal()

    @rx.event
    def open_delete_client_modal(self, client: Client):
        self.client_to_delete = client
        self.show_delete_client_modal = True

    @rx.event
    def close_delete_client_modal(self):
        self.show_delete_client_modal = False
        self.client_to_delete = None

    @rx.event
    def delete_client(self):
        if self.client_to_delete:
            self.clients = [
                c for c in self.clients if c["id"] != self.client_to_delete["id"]
            ]
            if self.selected_client_id == self.client_to_delete["id"] and self.clients:
                self.selected_client_id = self.clients[0]["id"]
            elif not self.clients:
                self.selected_client_id = -1
            self.close_delete_client_modal()

    @rx.event
    def view_client_domains(self, client_id: int):
        self.selected_client_id = client_id
        return rx.redirect(f"/clients/{client_id}/domains")

    @rx.event
    def on_load(self):
        params = self.router.page.params
        client_id_param = params.get("client_id_param")
        if client_id_param and (not client_id_param.startswith("[")):
            try:
                self.selected_client_id = int(client_id_param)
            except (ValueError, TypeError) as e:
                logging.exception(f"Error setting client_id from param: {e}")
                if self.clients:
                    self.selected_client_id = self.clients[0]["id"]
                else:
                    self.selected_client_id = -1