PROPERTY_NAME = "customStyle"


class Style():
    # A component is running, enabled, or armed
    ON = "on"

    # A component is disabled, not running, or disarmed, but could be enabled through this widget
    OFF = "off"

    # A component is disabled, not expected to have any effect or perform its function because of
    # some external factor, either another widget or something external to the gui
    # For example, a the arm button when the pi is not connected
    INACTIVE = "inactive"
