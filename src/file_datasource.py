from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.aggregated_data import AggregatedData
from domain.parking import Parking


class FileDatasource:
    def __init__(self, accelerometer_filename: str, gps_filename: str, parking_filename: str) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        self.accelerometer_file = None
        self.gps_file = None
        self.parking_file = None
        self.accelerometer_reader = None
        self.gps_reader = None
        self.parking_reader = None

    def startReading(self):
        """Метод повинен викликатись перед початком читання даних"""
        self.accelerometer_file = open(self.accelerometer_filename, 'r')
        self.gps_file = open(self.gps_filename, 'r')
        self.parking_file = open(self.parking_filename, 'r')
        self.accelerometer_reader = reader(self.accelerometer_file)
        self.gps_reader = reader(self.gps_file)
        self.parking_reader = reader(self.parking_file)

        # Пропускаємо заголовок файлів
        next(self.accelerometer_reader, None)
        next(self.gps_reader, None)
        next(self.parking_reader, None)

    def read_accelerometer(self):
        try:
            acc_data = next(self.accelerometer_reader)
        except StopIteration:
            self.accelerometer_file.seek(0)
            next(self.accelerometer_reader)
            acc_data = next(self.accelerometer_reader)

        return Accelerometer(int(acc_data[0]), int(acc_data[1]), int(acc_data[2]))

    def read_gps(self):
        try:
            gps_data = next(self.gps_reader)
        except StopIteration:
            self.gps_file.seek(0)
            next(self.gps_reader)
            gps_data = next(self.gps_reader)

        return Gps(float(gps_data[0]), float(gps_data[1]))

    def read_parking(self):
        try:
            parking_data = next(self.parking_reader)
        except StopIteration:
            self.parking_file.seek(0)
            next(self.parking_reader)
            parking_data = next(self.parking_reader)

        return Parking(int(parking_data[0]), Gps(float(parking_data[1]), float(parking_data[2])))

    def read_aggregated_data(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        accelerometer = self.read_accelerometer()
        gps = self.read_gps()

        return AggregatedData(accelerometer, gps, datetime.now())

    def stopReading(self):
        """Метод повинен викликатись для закінчення читання даних"""
        if self.accelerometer_file:
            self.accelerometer_file.close()
            self.accelerometer_file = None

        if self.gps_file:
            self.gps_file.close()
            self.gps_file = None

        if self.parking_file:
            self.parking_file.close()
            self.parking_file = None
