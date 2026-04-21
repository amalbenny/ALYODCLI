import time
from ALYODCLI import Activate

def run_tests(cli):
    # Runs a visual test suite of all components.
    
    print("\n", cli.style.paint(" AlyodCLI Test Suite ", "bg_magenta", "white", "bold"))
    cli.widgets.hr(width=40, char="=")
    
    # 1. Test Bullets & HR
    print(cli.style.paint("\nWidgets: Bullets", "bold"))
    cli.widgets.bullet("Environment checked")
    cli.widgets.bullet("Style matrix loaded", color="blue")
    cli.widgets.bullet("Dependencies verified", indent=2, color="yellow")
    
    # 2. Test Box
    print(cli.style.paint("\nLayout: Box", "bold"))
    cli.layout.box(["System Initialized", "All systems operational."], color="green")
    
    # 3. Test Table
    print(cli.paint("\nLayout: Table", "bold"))
    table_data = [
        {"Module": "Terminal", "Status": cli.style.paint("PASS", "green")},
        {"Module": "Style", "Status": cli.style.paint("PASS", "green")},
        {"Module": "Layout", "Status": cli.style.paint("WARN", "yellow")}
    ]
    cli.layout.table(table_data)
    
    # 4. Test Progress Bar
    print(cli.style.paint("\nWidgets: Progress", "bold"))
    for i in range(11):
        cli.widgets.progress(i, 10, prefix="Processing Data")
        time.sleep(0.1)
        
    # 5. Test Navigation
    print(cli.style.paint("\nWidgets: Navigation", "bold"))
    print(cli.style.paint("Use Arrow Keys to move (Gaming and Vim naivagtion is also supported), Enter to select.", "dim"))
    
    try:
        choice = cli.widgets.navigation(["Start Server", "Deploy Database", "Run Diagnostics", "Exit"])
        print(f"\nYou selected: {cli.style.paint(choice, 'green', 'bold')}")
    except KeyboardInterrupt:
        print("\nNavigation cancelled.")

cli= Activate()
run_tests(cli)
