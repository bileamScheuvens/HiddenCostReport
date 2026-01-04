def pytest_terminal_summary(terminalreporter, exitstatus, config):
    terminalreporter.ensure_newline()
    x = getattr(config, "metric_coverage", "")
    terminalreporter.write(x+"\n")
