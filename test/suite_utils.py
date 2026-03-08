stdout_handler_added = False


def enable_stdout_logs(level: int) -> None:
    global stdout_handler_added
    import sys
    import logging

    if not stdout_handler_added:
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        stdout_handler_added = True

    logging.getLogger().setLevel(level)
