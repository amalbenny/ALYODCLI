from ALYODCLI import Activate, __version__
import time
# Initialize the CLI
cli = Activate()

def main():

    
    # 1. Show a beautiful header
    print("\n")
    cli.layout.box([
        "ALYOD CLI 🎨",
        f"Version {__version__}",
        "System Status: Operational"
    ], color="cyan", align="center")
    
    # 2. Show some bullets
    print("\n" + cli.style.paint("Features Loaded:", "bold", "underline"))
    cli.widgets.bullet("ANSI Color Matrix", color="green")
    cli.widgets.bullet("Layout Engine (Boxes/Tables)", color="blue")
    cli.widgets.bullet("Interactive Widgets", color="magenta")
    
    # 3. Show a table
    print("\n" + cli.paint("Module Inventory:", "bold", "underline"))
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

if __name__ == "__main__":
    main()