# __main__.py
import sys
from pathlib import Path

import streamlit.web.cli as stcli


def main() -> None:
    """
    Sets up the environment to run a Streamlit application by modifying
    system arguments and initiating the Streamlit CLI.

    This function determines the current directory of the script, constructs
    the path to the Streamlit app, updates the system arguments to run the
    app, and then executes the Streamlit command-line interface to start the
    application.

    Exits the program when the Streamlit application exits, passing the
    appropriate exit code.
    """

    current_dir = Path(__file__).parent
    streamlit_app_path = current_dir / "app.py"

    sys.argv = ["streamlit", "run", str(
        streamlit_app_path), "--server.port", "7860", "--server.maxUploadSize", "10"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
