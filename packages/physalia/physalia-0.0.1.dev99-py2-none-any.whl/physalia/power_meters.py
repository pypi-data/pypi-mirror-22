"""Models to interact with different power meters."""

import abc
import time
import click
from physalia.third_party.monsoon import Monsoon
from physalia.third_party import monsoon_async
from physalia.utils import android


class PowerMeter(object):
    """Abstract class for interaction with a power monitor."""

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def start(self):
        """Start measuring energy consumption."""
        return

    @abc.abstractmethod
    def stop(self):
        """Stop measuring energy consumption.

        Returns:
            Energy consumption in Joules

        """
        return


class EmulatedPowerMeter(PowerMeter):
    """PowerMeter implementation to emulate a power monitor."""

    def __init__(self):  # noqa: D102
        self.start_time = None

    def start(self):
        """Start measuring energy consumption."""
        self.start_time = time.time()

    def stop(self):
        """Stop measuring energy consumption.

        Returns:
            Energy consumption in Joules

        """
        duration = time.time() - self.start_time
        energy_consumption = duration
        return energy_consumption, duration

class MonsoonPowerMeter(PowerMeter):
    """PowerMeter implementation for Monsoon.

    Make sure the Android device has Passlock disabled.
    Your server and device have to be connected to the same network.
    """

    def __init__(self, voltage=3.8, sample_hz=50000, serial=12886):  # noqa: D102
        self.monsoon = None
        self.monsoon_reader = None
        self.monsoon_data = None
        self.voltage = None
        self.serial = None
        self.sample_hz = sample_hz

        self.setup_monsoon(voltage, serial)
        click.secho(
            "Monsoon is ready.",
            fg='green'
        )
        if not android.is_android_device_available():
            click.secho(
                "You can now turn the phone on.",
                fg='blue'
            )
        for _ in range(50):
            click.secho(
                "Waiting for an Android device...",
                fg='blue'
            )
            time.sleep(3)
            if android.is_android_device_available():
                click.secho(
                    "Found a {}!".format(android.get_device_model()),
                    fg='green'
                )
                break
        android.connect_adb_through_wifi()
        self.monsoon_usb_enabled(False)
        if android.is_locked():
            click.secho(
                "Device seems to be locked. "
                "Disabling Passlock is recommended!",
                fg='yellow'
            )

    def setup_monsoon(self, voltage, serial):
        """Set up monsoon.

        Args:
            voltage: Voltage output of the power monitor.
            serial: serial number of the power monitor.
        """
        click.secho(
            "Setting up Monsoon {} with {}V...".format(
                serial, voltage
            ),
            fg='blue'
        )

        self.serial = serial
        self.voltage = voltage
        self.monsoon = Monsoon(serial=self.serial)
        self.monsoon.set_voltage(self.voltage)
        if android.is_android_device_available():
            android.reconnect_adb_through_usb()
        self.monsoon_usb_enabled(True)

    def monsoon_usb_enabled(self, enabled):
        """Enable/disable monsoon's usb port."""
        # pylint: disable=too-many-function-args
        # something is conflicting with timeout_decorator
        self.monsoon.usb(
            self.monsoon,
            {True:'on', False:'off'}[enabled]
        )

    def start(self):
        """Start measuring energy consumption."""
        self.monsoon_reader = monsoon_async.MonsoonReader(
            self.monsoon,
            self.sample_hz
        )
        self.monsoon_reader.start()

    def stop(self):
        """Stop measuring."""
        self.monsoon_reader.stop()
        data_points = self.monsoon_reader.data.data_points
        sample_hz = self.monsoon_reader.data.hz
        energy_consumption = sum(data_points)/sample_hz/1000
        duration = len(data_points)/sample_hz
        return energy_consumption, duration
