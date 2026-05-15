from PySide6.QtCore import QObject, QTimer, Signal

from models.signal_model import SignalModel


class MainViewModel(QObject):
    plot_updated = Signal(object, object)

    def __init__(self):
        super().__init__()

        # TODO 1:
        # Create the SignalModel.
        # Use:
        # - sampling_rate=1000
        # - duration=100
        # - window_size=5000
        # - step_size=20
        self.model = SignalModel(sampling_rate=1000, duration=100, window_size=5000, step_size=20)


        # TODO 2:
        # Initialize:
        # - current_index
        # - is_plotting
        self.current_index = 0
        self.is_plotting = False

        # TODO 3:
        # Create a QTimer and connect its timeout signal
        # to self.update_plot
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)

    def start_plotting(self):
        # TODO 4:
        # Start plotting only if plotting is currently stopped.
        # Then:
        # - set is_plotting to True
        # - start the timer with an interval of 10 ms
        if not self.is_plotting:
            self.is_plotting = True
            self.timer.start(10)

    def stop_plotting(self):
        # TODO 5:
        # Stop plotting only if plotting is currently running.
        # Then:
        # - set is_plotting to False
        # - stop the timer
        if self.is_plotting:
            self.is_plotting = False
            self.timer.stop()

    def update_plot(self):
        if not self.model.has_enough_data(self.current_index):
            self.current_index = 0

        x, y = self.model.get_window(self.current_index)
        self.plot_updated.emit(x, y)

        self.current_index += self.model.step_size