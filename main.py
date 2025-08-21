import argparse
import asyncio
import sys

from src.application import Application
from src.utils.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


def parse_args():
    """
    Analyse les paramètres de ligne de commande.
    """
    parser = argparse.ArgumentParser(description="Client IA Xiaozhi")
    parser.add_argument(
        "--mode",
        choices=["gui", "cli"],
        default="gui",
        help="Mode d'exécution : gui (interface graphique) ou cli (ligne de commande)",
    )
    parser.add_argument(
        "--protocol",
        choices=["mqtt", "websocket"],
        default="websocket",
        help="Protocole de communication : mqtt ou websocket",
    )
    parser.add_argument(
        "--skip-activation",
        action="store_true",
        help="Ignorer l'activation et démarrer directement l'application (débogage uniquement)",
    )
    return parser.parse_args()


async def handle_activation(mode: str) -> bool:
    """Gère le processus d'activation de l'appareil en utilisant la boucle d'événements existante.

    Args:
        mode: mode d'exécution, "gui" ou "cli"

    Returns:
        bool: succès de l'activation
    """
    try:
        from src.core.system_initializer import SystemInitializer

        logger.info("Début de la vérification du processus d'activation de l'appareil...")

        system_initializer = SystemInitializer()
        # Utilise le traitement d'activation de SystemInitializer, compatible GUI/CLI
        result = await system_initializer.handle_activation_process(mode=mode)
        success = bool(result.get("is_activated", False))
        logger.info(f"Processus d'activation terminé, résultat : {success}")
        return success
    except Exception as e:
        logger.error(f"Exception durant le processus d'activation : {e}", exc_info=True)
        return False


async def start_app(mode: str, protocol: str, skip_activation: bool) -> int:
    """
    Point d'entrée unifié pour démarrer l'application (dans une boucle d'événements existante).
    """
    logger.info("Démarrage du client IA Xiaozhi")

    # Gestion du processus d'activation
    if not skip_activation:
        activation_success = await handle_activation(mode)
        if not activation_success:
            logger.error("Échec de l'activation de l'appareil, arrêt du programme")
            return 1
    else:
        logger.warning("Processus d'activation ignoré (mode débogage)")

    # Crée et démarre l'application
    app = Application.get_instance()
    return await app.run(mode=mode, protocol=protocol)


if __name__ == "__main__":
    exit_code = 1
    try:
        args = parse_args()
        setup_logging()

        if args.mode == "gui":
            # En mode GUI, main crée l'application QApplication et la boucle qasync
            try:
                import qasync
                from PyQt5.QtWidgets import QApplication
            except ImportError as e:
                logger.error(f"Le mode GUI nécessite les bibliothèques qasync et PyQt5 : {e}")
                sys.exit(1)

            qt_app = QApplication.instance() or QApplication(sys.argv)

            loop = qasync.QEventLoop(qt_app)
            asyncio.set_event_loop(loop)
            logger.info("Boucle d'événements qasync créée dans main")

            with loop:
                exit_code = loop.run_until_complete(
                    start_app(args.mode, args.protocol, args.skip_activation)
                )
        else:
            # Le mode CLI utilise la boucle asyncio standard
            exit_code = asyncio.run(
                start_app(args.mode, args.protocol, args.skip_activation)
            )

    except KeyboardInterrupt:
        logger.info("Programme interrompu par l'utilisateur")
        exit_code = 0
    except Exception as e:
        logger.error(f"Arrêt anormal du programme : {e}", exc_info=True)
        exit_code = 1
    finally:
        sys.exit(exit_code)
