from UI.menu import MenuEngine


def main() -> None:
    mn = MenuEngine()
    try:
        mn.run()
    except KeyboardInterrupt:
        print("\n")
        mn.exit_menu()


if __name__ == "__main__":
    main()
    # monopoly_sample()
