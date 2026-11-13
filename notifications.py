import flet as ft
import json
import os
import requests
import threading
from core import theme
from core.languages import Language

# --- Global Configurations ---
FIREBASE_URL = "https://satine-2f698-default-rtdb.firebaseio.com/noti.json"
NOTIFICATIONS_FILE = "notifications.json"
COUNT_FILE = "last_count.json"


def get_loc(page: ft.Page) -> Language:
    """Reads the persisted language choice so this screen matches the main view."""
    try:
        saved = page.client_storage.get("lang") or "ar"
    except Exception:
        saved = "ar"
    return Language(saved)


class NotificationCard(ft.Container):
    """Encapsulates the notification card layout, styling, and external image launcher."""
    def __init__(self, page: ft.Page, loc: Language, text: str, amount: float, noti_type: str, date: str, bank, img_url: str = None):
        self.page = page

        # Configure icon and color based on notification type
        config = {
            "w": {"text": loc.t("notif_withdraw", amount=f"{amount:,.0f}"), "color": theme.DANGER, "chip": theme.DANGER_SOFT, "icon": ft.icons.CALL_MADE_ROUNDED},
            "d": {"text": loc.t("notif_deposit", amount=f"{amount:,.0f}"), "color": theme.PRIMARY_DARK, "chip": theme.PRIMARY_SOFT, "icon": ft.icons.CALL_RECEIVED_ROUNDED},
            "don": {"text": loc.t("notif_donation", amount=f"{amount:,.0f}"), "color": theme.GOLD_DARK, "chip": theme.GOLD_SOFT, "icon": ft.icons.MONETIZATION_ON_ROUNDED},
            "s": {"text": loc.t("notif_new_sub"), "color": theme.PRIMARY_DARK, "chip": theme.PRIMARY_SOFT, "icon": ft.icons.PERSON_ADD_ALT_1_ROUNDED},
            "u": {"text": loc.t("notif_unsub"), "color": theme.GOLD_DARK, "chip": theme.GOLD_SOFT, "icon": ft.icons.PERSON_REMOVE_ALT_1_ROUNDED}
        }.get(noti_type, {"text": loc.t("notif_general"), "color": theme.TEXT_SECONDARY, "chip": theme.SURFACE_ALT, "icon": ft.icons.NOTIFICATIONS_OUTLINED})

        # Main layout elements: Title and Notification text first
        card_columns = [
            ft.Text(config["text"], color=theme.TEXT_PRIMARY, weight=ft.FontWeight.BOLD, size=15),
            ft.Text(text, color=theme.TEXT_SECONDARY, size=14)
        ]

        # Verify if img_url is valid and non-empty string
        if img_url and isinstance(img_url, str) and img_url.strip():
            # check if the image is bank notification or not
            if bank == True:
                img_text = loc.t("bank_notif")
                img_txt_col = theme.PRIMARY_DARK
                img_icon = "check_circle"
            else:
                img_text = loc.t("view_image")
                img_txt_col = theme.GOLD_DARK
                img_icon = "image"
            # Compact "Bankak Notification" button with explicit icon size control
            view_img_btn = ft.TextButton(
                content=ft.Row(
                    controls=[
                        ft.Icon(img_icon, size=16, color=img_txt_col),
                        ft.Text(img_text, color=img_txt_col, size=13)
                    ],
                    spacing=5,
                    tight=True
                ),
                style=ft.ButtonStyle(
                    padding=ft.padding.all(0)
                ),
                on_click=lambda _: self._launch_image_url(img_url.strip())
            )
            card_columns.append(
                ft.Container(
                    content=view_img_btn,
                    margin=ft.margin.only(top=2, bottom=2)
                )
            )

        # Append the date at the very bottom
        card_columns.append(ft.Text(loc.t("on_day", date=date), color=theme.TEXT_MUTED, size=11))

        super().__init__(
            padding=ft.padding.only(right=12, left=12, top=12, bottom=15),
            bgcolor=theme.SURFACE,
            border_radius=16,
            border=ft.border.all(1, theme.BORDER),
            margin=ft.margin.only(bottom=10)
        )

        self.content = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(config["icon"], color=config["color"], size=20),
                    padding=10,
                    bgcolor=config["chip"],
                    border_radius=12
                ),
                ft.Column(
                    controls=card_columns,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=3,
                    expand=True
                )
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.START
        )

    def _launch_image_url(self, url: str):
        """Launches the image URL directly in the device's default browser to ensure 100% rendering success."""
        try:
            self.page.launch_url(url)
        except Exception:
            pass


class NotificationManager:
    """Handles data fetching, sorting, and local storage management using requests."""
    def __init__(self):
        self.url = FIREBASE_URL
        self.file_path = NOTIFICATIONS_FILE
        self.count_path = COUNT_FILE

    def fetch_sorted_notifications(self) -> list:
        """Fetches data from Firebase or local cache and returns a chronologically sorted list (newest first)."""
        data = None
        try:
            response = requests.get(self.url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data:
                    with open(self.count_path, "w") as f:
                        json.dump(len(data), f)
                    with open(self.file_path, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False)
        except Exception:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

        sorted_items = []
        if data and isinstance(data, dict):
            sorted_keys = sorted(data.keys(), reverse=True)
            for key in sorted_keys:
                if data[key]:
                    sorted_items.append(data[key])
        elif data and isinstance(data, list):
            sorted_items = list(reversed([item for item in data if item]))

        return sorted_items

    def send_notification(self, text: str, amount: float, noti_type: str, date: str, img_url: str = None) -> bool:
        """Sends a new notification using POST request."""
        payload = {
            "noti": text,
            "amount": amount,
            "type": noti_type,
            "date": date
        }
        if img_url and isinstance(img_url, str) and img_url.strip():
            payload["img"] = img_url.strip()

        try:
            response = requests.post(self.url, json=payload, timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    def check_new_notifications(self) -> bool:
        """Compares live data count with saved count to determine if there are new alerts."""
        try:
            res = requests.get(self.url, timeout=3).json()
            current_count = len(res) if res else 0
        except Exception:
            current_count = 0

        saved_count = 0
        if os.path.exists(self.count_path):
            try:
                with open(self.count_path, "r") as f:
                    content = f.read()
                    if content:
                        saved_count = json.loads(content)
            except (json.JSONDecodeError, ValueError):
                saved_count = 0

        return current_count > saved_count


class NotificationViewManager:
    """Manages the UI creation and thread handling for the notifications screen."""
    def __init__(self, page: ft.Page):
        self.page = page
        self.loc = get_loc(page)
        self.manager = NotificationManager()
        self.notif_list = ft.ListView(expand=True, spacing=0)
        self.loading_ring = ft.ProgressRing(color=theme.PRIMARY)
        self.loading_container = ft.Container(content=self.loading_ring, alignment=ft.alignment.center, expand=True)
        self.view = ft.View("/notifications", bgcolor=theme.BG, padding=20, controls=[self.loading_container])

    def build_view(self) -> ft.View:
        threading.Thread(target=self._load_data_thread, daemon=True).start()
        return self.view

    def _load_data_thread(self):
        total_deposit = 0
        total_withdraw = 0

        items = self.manager.fetch_sorted_notifications()

        for item in items:
            self.notif_list.controls.append(
                NotificationCard(
                    page=self.page,
                    loc=self.loc,
                    text=item.get('noti', '') if self.page.client_storage.get("lang") == "ar" else item.get("en_noti"),
                    amount=item.get('amount', 0),
                    noti_type=item.get('type', ''),
                    date=item.get('date', ''),
                    bank=item.get('bank', True),
                    img_url=item.get('img')
                )
            )
            if item.get("type") == "d":
                total_deposit += item.get("amount", 0)
            elif item.get("type") == "w":
                total_withdraw += item.get("amount", 0)

        header = ft.Container(
            gradient=ft.LinearGradient(
                begin=ft.alignment.top_left,
                end=ft.alignment.bottom_right,
                colors=theme.GRADIENT_HEADER
            ),
            content=ft.Row([
                ft.Column([
                    ft.Text(self.loc.t("total_deposits"), color=theme.ON_HEADER_MUTED, size=14),
                    ft.Text(f"{total_deposit:,.0f}", color=theme.ON_HEADER, size=20, weight=ft.FontWeight.BOLD)
                ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.VerticalDivider(width=1, color=ft.colors.with_opacity(0.25, ft.colors.WHITE)),
                ft.Column([
                    ft.Text(self.loc.t("total_withdrawals"), color=theme.ON_HEADER_MUTED, size=14),
                    ft.Text(f"{total_withdraw:,.0f}", color=theme.ON_HEADER, size=20, weight=ft.FontWeight.BOLD)
                ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ]),
            padding=20,
            border_radius=20,
            margin=ft.margin.only(top=30, bottom=15)
        )

        self.view.controls = [header, self.notif_list]
        self.view.floating_action_button = ft.FloatingActionButton(
            icon=ft.icons.ARROW_FORWARD,
            bgcolor=theme.PRIMARY,
            on_click=lambda _: self.page.go("/"),
            width=40, height=40
        )
        self.page.update()


# --- Helper Functions for External Usage ---
def get_notifications_view(page: ft.Page):
    """Bridge function to match your routing system."""
    view_manager = NotificationViewManager(page)
    return view_manager.build_view()


def build_notification_icon(page: ft.Page):
    """Generates the notification button with a dynamic unread badge."""
    manager = NotificationManager()
    has_new = manager.check_new_notifications()

    return ft.Stack([
        ft.IconButton(
            icon=ft.icons.NOTIFICATIONS,
            icon_color=theme.ON_HEADER_MUTED,
            on_click=lambda _: page.go("/notifications")
        ),
        ft.Container(
            content=ft.CircleAvatar(bgcolor=theme.DANGER, radius=5),
            visible=has_new,
            top=5,
            right=5
        )
    ])
