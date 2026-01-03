# tests/test_logging_and_sentry.py
import logging
from app.utils import logging_config, sentry_config


def test_setup_logging_initializes_logger(monkeypatch, capsys):
    # Forcer un LOG_LEVEL connu
    monkeypatch.setenv("LOG_LEVEL", "INFO")

    # Mock init_sentry pour ne pas appeler le vrai Sentry
    called = {}

    def fake_init_sentry():
        called["init"] = True

    monkeypatch.setattr(logging_config, "init_sentry", fake_init_sentry)

    logger = logging_config.setup_logging()

    # init_sentry doit avoir été appelé
    assert called.get("init") is True

    # logger principal doit exister et être de niveau INFO
    assert isinstance(logger, logging.Logger)
    assert logger.name == "epicevents"
    assert logger.level == logging.INFO

    # log d'info ne doit pas planter
    logger.info("Test info")
    # Pas obligatoire d'asserter sur le texte, l’essentiel est que ça ne plante pas
    capsys.readouterr()


def test_log_levels_with_mocked_sentry(monkeypatch, capsys):
    # Mock capture_exception et capture_message
    captured_exc = {}
    captured_msg = {}

    def fake_capture_exception(exc, context=None):
        captured_exc["exception"] = exc
        captured_exc["context"] = context

    def fake_capture_message(msg, level="warning"):
        captured_msg["message"] = msg
        captured_msg["level"] = level

    monkeypatch.setattr(logging_config, "capture_exception", fake_capture_exception)
    monkeypatch.setattr(sentry_config, "capture_message", fake_capture_message)

    # S'assurer que le logger existe
    logging_config.setup_logging()

    # log_info
    logging_config.log_info("Info message")
    # log_warning -> doit appeler capture_message
    logging_config.log_warning("Warn message")
    # log_error avec exception >>> doit appeler capture_exception
    try:
        raise ValueError("Boom")
    except ValueError as e:
        logging_config.log_error("Erreur critique", e)

    # Vérifications Sentry mocké
    assert captured_msg["message"] == "Warn message"
    assert captured_msg["level"] == "warning"

    assert isinstance(captured_exc["exception"], ValueError)
    assert captured_exc["context"]["message"] == "Erreur critique"


def test_init_sentry_without_dsn(monkeypatch, capsys):
    # SENTRY_DSN non défini -> pas d’init
    monkeypatch.delenv("SENTRY_DSN", raising=False)

    sentry_config.init_sentry()
    out = capsys.readouterr()
    assert "SENTRY_DSN non configuré" in out.out


class DummySentry:
    def __init__(self):
        self.inited = False
        self.captured_exc = []
        self.captured_msg = []

    def init(self, **kwargs):
        self.inited = True
        self.kwargs = kwargs

    def capture_exception(self, exc):
        self.captured_exc.append(exc)

    def capture_message(self, msg, level="error"):
        self.captured_msg.append((msg, level))

    @staticmethod
    def push_scope():
        # contexte minimal pour le with
        class ScopeCtx:
            def __enter__(self):
                class Scope:
                    def set_extra(self, k, v):
                        pass
                return Scope()

            def __exit__(self, exc_type, exc, tb):
                pass

        return ScopeCtx()


def test_init_and_capture_with_dsn(monkeypatch, capsys):
    dummy = DummySentry()
    monkeypatch.setenv("SENTRY_DSN", "http://testdsn")
    monkeypatch.setattr(sentry_config, "sentry_sdk", dummy)

    sentry_config.init_sentry()
    assert dummy.inited is True

    # capture_exception
    exc = ValueError("Test error")
    sentry_config.capture_exception(exc, {"key": "value"})
    assert dummy.captured_exc[0] is exc

    # capture_message
    sentry_config.capture_message("Hello", level="info")
    assert dummy.captured_msg[0] == ("Hello", "info")
