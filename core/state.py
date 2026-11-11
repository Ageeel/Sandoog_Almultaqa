from core.languages import Language

class AppState:
	def __init__(self, page):
		self.page = page
		saved = page.client_storage.get("lang") or "ar"
		self.loc = Language(saved)

	def set_lang(self, lang: str):
		self.loc.set_lang(lang)
		try:
			self.page.client_storage.set("lang", lang)
		except Exception:
			pass

	def toggle_lang(self):
		self.loc.toggle()
		try:
			self.page.client_storage.set("lang", self.loc.lang)
		except Exception:
			pass
