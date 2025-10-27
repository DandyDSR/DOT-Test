import reflex as rx
from typing import TypedDict, Optional
import logging


class Domain(TypedDict):
    id: int
    client_id: int
    domain_name: str
    gsc_connected: bool
    ga4_connected: bool
    gsc_property_uri: Optional[str]
    ga4_property_id: Optional[str]


class DomainState(rx.State):
    domains: list[Domain] = [
        {
            "id": 101,
            "client_id": 1,
            "domain_name": "reflex.dev",
            "gsc_connected": True,
            "ga4_connected": False,
            "gsc_property_uri": "sc-domain:reflex.dev",
            "ga4_property_id": None,
        },
        {
            "id": 102,
            "client_id": 1,
            "domain_name": "docs.reflex.dev",
            "gsc_connected": True,
            "ga4_connected": True,
            "gsc_property_uri": "https://docs.reflex.dev/",
            "ga4_property_id": "123456789",
        },
        {
            "id": 201,
            "client_id": 2,
            "domain_name": "dandymarketing.co.uk",
            "gsc_connected": False,
            "ga4_connected": False,
            "gsc_property_uri": None,
            "ga4_property_id": None,
        },
    ]
    show_add_domain_modal: bool = False
    show_edit_domain_modal: bool = False
    show_delete_domain_modal: bool = False
    domain_to_edit: Domain | None = None
    domain_to_delete: Domain | None = None
    domain_to_connect: Domain | None = None
    service_to_connect: str = ""

    @rx.event
    def on_load(self):
        return

    @rx.event
    def open_add_domain_modal(self):
        self.show_add_domain_modal = True

    @rx.event
    def close_add_domain_modal(self):
        self.show_add_domain_modal = False

    @rx.event
    def add_domain(self, form_data: dict):
        new_id = max([d["id"] for d in self.domains]) + 1 if self.domains else 1
        client_id_param = self.router.page.params.get("client_id_param")
        if not client_id_param:
            return
        new_domain: Domain = {
            "id": new_id,
            "client_id": int(client_id_param),
            "domain_name": form_data["domain_name"],
            "gsc_connected": False,
            "ga4_connected": False,
            "gsc_property_uri": None,
            "ga4_property_id": None,
        }
        self.domains.append(new_domain)
        self.show_add_domain_modal = False

    @rx.event
    def open_edit_domain_modal(self, domain: Domain):
        self.domain_to_edit = domain
        self.show_edit_domain_modal = True

    @rx.event
    def close_edit_domain_modal(self):
        self.show_edit_domain_modal = False
        self.domain_to_edit = None

    @rx.event
    def update_domain(self, form_data: dict):
        if self.domain_to_edit:
            domain_id_to_update = self.domain_to_edit["id"]
            self.domains = [
                {**d, "domain_name": form_data["domain_name"]}
                if d["id"] == domain_id_to_update
                else d
                for d in self.domains
            ]
            self.close_edit_domain_modal()

    @rx.event
    def open_delete_domain_modal(self, domain: Domain):
        self.domain_to_delete = domain
        self.show_delete_domain_modal = True

    @rx.event
    def close_delete_domain_modal(self):
        self.show_delete_domain_modal = False
        self.domain_to_delete = None

    @rx.event
    def delete_domain(self):
        if self.domain_to_delete:
            self.domains = [
                d for d in self.domains if d["id"] != self.domain_to_delete["id"]
            ]
            self.close_delete_domain_modal()

    @rx.event
    def view_domain_analytics(self, domain_id: int):
        client_id_param = self.router.page.params.get("client_id_param")
        return rx.redirect(f"/clients/{client_id_param}/domains/{domain_id}/analytics")

    @rx.event
    def initiate_connection(self, domain: Domain, service: str):
        self.domain_to_connect = domain
        self.service_to_connect = service
        if service == "gsc":
            from app.services.gsc_service import get_gsc_auth_url

            auth_url = get_gsc_auth_url()
            if auth_url:
                return rx.redirect(auth_url)
            else:
                return rx.toast(
                    "GSC integration not configured. Please add client_secret.json.",
                    duration=5000,
                )
        elif service == "ga4":
            print(f"Initiating GA4 connection for {domain['domain_name']}")
            return rx.toast("GA4 integration is not yet implemented.", duration=3000)

    @rx.event
    def handle_oauth_callback(self):
        params = self.router.page.params
        code = params.get("code")
        state_str = params.get("state")
        if not code or not self.domain_to_connect or (not self.service_to_connect):
            return
        client_id_for_redirect = self.domain_to_connect.get("client_id")
        if self.service_to_connect == "gsc":
            from app.services.gsc_service import get_gsc_credentials

            try:
                credentials = get_gsc_credentials(code)
                for i, d in enumerate(self.domains):
                    if d["id"] == self.domain_to_connect["id"]:
                        self.domains[i]["gsc_connected"] = True
                        break
                self.domain_to_connect = None
                self.service_to_connect = ""
                return rx.redirect(f"/clients/{client_id_for_redirect}/domains")
            except Exception as e:
                logging.exception(f"GSC OAuth failed: {e}")

    @rx.var
    def selected_client_domains(self) -> list[Domain]:
        client_id_param = self.router.page.params.get("client_id_param")
        if not client_id_param:
            return []
        try:
            current_client_id = int(client_id_param)
            return [d for d in self.domains if d["client_id"] == current_client_id]
        except (ValueError, TypeError) as e:
            logging.exception(f"Error: {e}")
            return []