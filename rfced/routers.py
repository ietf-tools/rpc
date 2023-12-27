class RfcedRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == "rfced":
            return "rfced"
        else:
            return None
    def db_for_write(self, model, **hints):
        if model._meta.app_label == "rfced":
            return "rfced"
        else:
            return None
