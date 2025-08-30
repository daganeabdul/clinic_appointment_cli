from colorama import Fore, Style, init
from cli.menu import patient_menu, doctor_menu, admin_menu, MAIN_MENU, print_menu

def main():
    init(autoreset=True)  # this colorama
    ACTIONS = {
        "1": patient_menu,
        "2": doctor_menu,
        "3": admin_menu,
        "4": lambda: "EXIT",
    }
    while True:
        print(Fore.BLUE + "\n=== Clinic Appointment CLI ===" + Style.RESET_ALL)
        print_menu(MAIN_MENU)  # tuple usage
        choice = input("Choose role: ").strip()
        action = ACTIONS.get(choice)
        if not action:
            print(Fore.RED + "Invalid option." + Style.RESET_ALL)
            continue
        if action() == "EXIT":
            print(Fore.CYAN + "Goodbye!" + Style.RESET_ALL)
            break
        action()

if __name__ == "__main__":
    main()
