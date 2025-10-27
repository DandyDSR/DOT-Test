import reflex as rx
from reflex_google_auth import GoogleAuthState


class AuthState(GoogleAuthState):
    @rx.event
    def on_load(self):
        if self.token_is_valid:
            print("User is logged in.")
        else:
            print("User is not logged in.")
        return