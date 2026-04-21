from ALYODCLI import Activate
import time


def main():
    # Initialize the CLI
    cli = Activate()
    
    # 1. Show a beautiful header
    print("\n")
    cli.layout.box([
        "ALYOD CLI FORMATTER",
        "Version 0.1.0",
        "System Status: Operational"
    ], color="cyan", align="center")
    
    # 2. Show some bullets
    print("\n" + cli.style.paint("Features Loaded:", "bold", "underline"))
    cli.widgets.bullet("ANSI Color Matrix", color="green")
    cli.widgets.bullet("Layout Engine (Boxes/Tables)", color="blue")
    cli.widgets.bullet("Interactive Widgets", color="magenta")
    
    # 3. Show a table
    print("\n" + cli.style.paint("Module Inventory:", "bold", "underline"))
    data = [
        {"Module": "Terminal", "Version": "1.0", "Status": cli.style.paint("STABLE", "green")},
        {"Module": "Layout", "Version": "0.9", "Status": cli.style.paint("BETA", "yellow")},
        {"Module": "Widgets", "Version": "1.1", "Status": cli.style.paint("STABLE", "green")}
    ]
    cli.layout.table(data)
    
    # 4. Progress bar simulation
    print("\n" + cli.style.paint("Syncing Data...", "bold"))
    for i in range(101):
        cli.widgets.progress(i, 100, prefix="Downloading")
        time.sleep(0.02)
        
    print("\n" + cli.style.paint("Setup Complete!", "green", "bold"))

if __name__ == "__main__":
    main()

