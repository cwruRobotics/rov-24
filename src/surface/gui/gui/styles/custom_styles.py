class Style():
    """Represents a single class that can be applied to gui objects to change their appearance."""

    PROPERTY_NAME: str


class WidgetState(Style):
    """Represents the state of a widget that can be alternately active or inactive."""

    PROPERTY_NAME = "widgetState"

    # A component is running, enabled, or armed
    ON = "on"

    # A component is disabled, not running, or disarmed, but could be enabled through this widget
    OFF = "off"

    # A component is disabled, not expected to have any effect or perform its function because of
    # some external factor, either another widget or something external to the gui
    # For example, a the arm button when the pi is not connected
    INACTIVE = "inactive"
