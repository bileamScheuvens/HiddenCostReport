def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Use terminal summary hook to print metric coverage."""
    terminalreporter.ensure_newline()
    terminalreporter.write(f"{getattr(config, "metric_coverage", "")}\n")
