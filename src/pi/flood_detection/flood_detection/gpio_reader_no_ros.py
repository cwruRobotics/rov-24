import lgpio


def main() -> None:
    # Pins used for GPIO
    detect1 = 17
    # GPIO Boilerplate
    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_input(h, detect1)

    data1 = lgpio.gpio_read(h, detect1)

    firstRun = True

    while True:
        # Read Data
        olddata1: int = data1

        data1 = lgpio.gpio_read(h, detect1)

        if data1 != olddata1 or firstRun:
            print("Pin 17: %s" % data1)

            if data1:
                print("\nBad Flooding Thing")

            firstRun = False


if __name__ == '__main__':
    main()
