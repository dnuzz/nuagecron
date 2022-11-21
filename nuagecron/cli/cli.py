from click import command, echo


@command('nuagecron')
def main():
    echo("Test main CLI")
