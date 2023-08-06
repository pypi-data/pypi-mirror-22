from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import six
import os
from os import listdir, path
from os.path import isfile, join
from functools import partial
from itertools import chain
import warnings

import numpy as np
import pims
from pims import FramesSequence, FramesSequenceND
from pims.utils.sort import natural_keys

from .widgets import CheckBox, DockWidget, VideoTimer, Slider
from .qt import (Qt, QtWidgets, QtGui, QtCore, Signal,
                 init_qtapp, start_qtapp)
from .display import Display
from .utils import (wrap_frames_sequence, recursive_subclasses,
                    to_rgb_uint8, memoize)

try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from moviepy.editor import VideoClip
except ImportError:
    VideoClip = None


class Viewer(QtWidgets.QMainWindow):
    """Viewer for displaying image sequences from pims readers.

    Parameters
    ----------
    reader : pims reader, optional
        Reader that loads images to be displayed.

    Notes
    -----
    The Viewer was based on `skimage.viewer.CollectionViewer`
    """
    dock_areas = {'top': Qt.TopDockWidgetArea,
                  'bottom': Qt.BottomDockWidgetArea,
                  'left': Qt.LeftDockWidgetArea,
                  'right': Qt.RightDockWidgetArea}
    _dropped = Signal(list)

    # signal on image change, so that plotting plugins can process the change
    original_image_changed = Signal()

    def __init__(self, reader=None, close_reader=True):
        self.plugins = []
        self._images = []
        self._img = None
        self._display = None
        self.sliders = dict()
        self.channel_tabs = None
        self.slider_dock = None
        self.is_multichannel = False
        self.is_playing = False
        self._index = dict()
        self.return_val = []
        self.reader = None
        self._close_reader = close_reader
        self.filename = None

        # Start main loop
        init_qtapp()
        super(Viewer, self).__init__()

        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowTitle("Python IMage Sequence Viewer")

        # list all pims reader classed in the "Open with" menu
        open_with_menu = QtWidgets.QMenu('Open with', self)
        for cls in set(chain(recursive_subclasses(FramesSequence),
                             recursive_subclasses(FramesSequenceND))):
            if hasattr(cls, 'no_reader'):
                continue
            open_with_menu.addAction(cls.__name__,
                                     partial(self.open_file, reader_cls=cls))

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('Open', self.open_file,
                                 Qt.CTRL + Qt.Key_O)
        self.file_menu.addMenu(open_with_menu)
        self.file_menu.addAction('Open next', self.open_next_file,
                                 Qt.CTRL + Qt.SHIFT + Qt.Key_O)
        self.file_menu.addAction('Open previous', self.open_previous_file,
                                 Qt.ALT + Qt.SHIFT + Qt.Key_O)
        self.file_menu.addAction('Close', self.close_reader)
        # self.file_menu.addAction('Save', self.save_file,
        #                          Qt.CTRL + Qt.Key_S)
        self.file_menu.addAction('Copy', self.to_clipboard,
                                 Qt.CTRL + Qt.Key_C)
        self.file_menu.addAction('Quit', self.close,
                                 Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.view_menu = QtWidgets.QMenu('&View', self)
        self._autoscale = QtWidgets.QAction('&Autoscale', self.view_menu,
                                            checkable=True)
        self._autoscale.setChecked(True)
        self._autoscale.toggled.connect(self.update_view)
        self.view_menu.addAction(self._autoscale)

        # list all Display subclasses in the View menu
        mode_menu = QtWidgets.QMenu('&Mode', self)
        mode_menu.addAction(Display.name + ' (default)',
                            partial(self.update_display,
                                    display_class=Display))
        for cls in recursive_subclasses(Display):
            if cls.available:
                mode_menu.addAction(cls.name, partial(self.update_display,
                                                      display_class=cls))
        self.view_menu.addMenu(mode_menu)

        resize_menu = QtWidgets.QMenu('&Resize', self)
        resize_menu.addAction('33 %', partial(self.resize_display, factor=1 / 3))
        resize_menu.addAction('50 %', partial(self.resize_display, factor=1 / 2))
        resize_menu.addAction('100 %', partial(self.resize_display, factor=1))
        resize_menu.addAction('200 %', partial(self.resize_display, factor=2))
        resize_menu.addAction('300 %', partial(self.resize_display, factor=3))
        self.view_menu.addMenu(resize_menu)

        play_menu = QtWidgets.QMenu('&Play', self)

        def _mult_fps(factor):
            self.fps *= factor

        play_menu.addAction('Start / stop', lambda: self.play(not self.is_playing))
        play_menu.addAction('Switch direction', partial(_mult_fps, factor=-1))
        play_menu.addAction('Faster', partial(_mult_fps, factor=1.2))
        play_menu.addAction('Slower', partial(_mult_fps, factor=0.8))
        self.view_menu.addMenu(play_menu)

        self.menuBar().addMenu(self.view_menu)

        # self.pipeline_menu = QtWidgets.QMenu('&Pipelines', self)
        # from pimsviewer.plugins import PipelinePlugin
        # for pipeline_obj in PipelinePlugin.instances:
        #     self.pipeline_menu.addAction(pipeline_obj.name,
        #                                  partial(self.add_plugin,
        #                                          pipeline_obj))
        # self.menuBar().addMenu(self.pipeline_menu)

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.setMinimumSize(800, 600)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred,
                           QtWidgets.QSizePolicy.Preferred)
        self.main_layout = QtWidgets.QGridLayout(self.main_widget)

        # make file dragging & dropping work
        self.setAcceptDrops(True)
        self._dropped.connect(self._open_dropped)

        self._status_bar = self.statusBar()

        # initialize the timer for video playback
        self._timer = VideoTimer(self)
        self._play_checkbox = None

        if reader is not None:
            self.update_reader(reader)

    def add_plugin(self, plugin):
        """Add Plugin to the Viewer"""
        plugin.attach(self)

        if plugin.dock:
            location = self.dock_areas[plugin.dock]
            dock_location = Qt.DockWidgetArea(location)
            dock = DockWidget()
            dock.setWidget(plugin)
            dock.setWindowTitle(plugin.name)
            dock.close_event_signal.connect(plugin.close)
            dock.setSizePolicy(QtWidgets.QSizePolicy.Fixed,
                               QtWidgets.QSizePolicy.MinimumExpanding)
            self.addDockWidget(dock_location, dock)

    def __add__(self, plugin):
        self.add_plugin(plugin)
        return self

    def show(self, main_window=True):
        """Show Viewer and attached ViewerPipelines."""
        self.move(0, 0)
        for p in self.plugins:
            p.show()
        super(Viewer, self).show()
        self.activateWindow()
        self.raise_()
        if main_window:
            start_qtapp()

        return self.return_val

    def closeEvent(self, event):
        for p in self.plugins:
            if hasattr(p, 'output'):
                self.return_val.append(p.output())
                p.close()
            else:
                self.return_val.append(None)
        if self._close_reader:
            self.close_reader()
        if self._display is not None:
            self._display.close()
        super(Viewer, self).closeEvent(event)

    # the update cascade: open_file -> update_reader -> update_display ->
    # update_original_image -> image -> update_view. Any function calls the next one,
    # but you can call for instance update_original_image to only update the image.

    def open_file(self, filename=None, reader_cls=None):
        """Open image file and update the viewer's reader"""
        if filename is None:
            try:
                cur_dir = os.path.dirname(self.reader.filename)
            except AttributeError:
                cur_dir = ''
            filename = QtWidgets.QFileDialog.getOpenFileName(directory=cur_dir)
            if isinstance(filename, tuple):
                # Handle discrepancy between PyQt4 and PySide APIs.
                filename = filename[0]
        if filename is None or len(filename) == 0:
            return
        if reader_cls is None:
            reader = pims.open(filename)
        else:
            reader = reader_cls(filename)
        if self.reader is not None:
            self.close_reader()
        self.update_reader(reader)
        self.status = 'Opened {}'.format(filename)
        self.filename = filename

    def open_next_file(self, forward=True):
        """
        Opens the next file in the current directory

        Parameters
        ----------
        forward : bool
            Cycle forward or backwards

        """
        if self.filename is None:
            self.open_file()

        current_directory = path.dirname(self.filename)
        file_list = self._get_all_files_in_dir(current_directory)
        if len(file_list) < 2:
            self.status = 'No file found for opening'
            return

        try:
            current_file_index = file_list.index(path.basename(self.filename))
        except ValueError:
            self.status = 'No file found for opening'
            return

        next_index = current_file_index + 1 if forward else current_file_index - 1
        try:
            next_file = file_list[next_index]
        except IndexError:
            next_index = 0 if forward else -1
            next_file = file_list[next_index]

        self.open_file(filename=path.join(current_directory, next_file))

    def open_previous_file(self):
        """
        Opens the previous file in the current directory
        """
        self.open_next_file(forward=False)

    def update_reader(self, reader):
        """Load a new reader into the Viewer."""
        if not isinstance(reader, FramesSequenceND):
            reader = wrap_frames_sequence(reader)
        self.reader = reader
        reader.iter_axes = 't'
        self._index = reader.default_coords.copy()

        # add color tabs
        if 'c' in reader.sizes:
            self.is_multichannel = True
            self.channel_tabs = QtWidgets.QTabBar(self)
            self.main_layout.addWidget(self.channel_tabs, 1, 0)
            self.channel_tabs.addTab('all')
            for c in range(reader.sizes['c']):
                self.channel_tabs.addTab(str(c))
                self.channel_tabs.setShape(QtWidgets.QTabBar.RoundedSouth)
                self.channel_tabs.currentChanged.connect(self.channel_tab_callback)
        else:
            self.is_multichannel = False

        # add sliders
        self.sliders = dict()
        for axis in reader.sizes:
            if axis in ['x', 'y', 'c'] or reader.sizes[axis] <= 1:
                continue
            self.sliders[axis] = Slider(axis, low=0, high=reader.sizes[axis] - 1,
                                        value=self._index[axis], update_on='release', value_type='int',
                                        callback=lambda x, y: self.set_index(y, x))

        if len(self.sliders) > 0:
            slider_widget = QtWidgets.QWidget()
            slider_layout = QtWidgets.QGridLayout(slider_widget)
            for i, axis in enumerate(self.sliders):
                slider_layout.addWidget(self.sliders[axis], i, 0)
                if axis == 't':
                    self._play_checkbox = CheckBox('play', self.is_playing,
                                                   callback=self.play_callback)
                    slider_layout.addWidget(self._play_checkbox, i, 1)

            self.slider_dock = QtWidgets.QDockWidget()
            self.slider_dock.setWidget(slider_widget)
            self.slider_dock.setWindowTitle('Axes sliders')
            self.slider_dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable |
                                         QtWidgets.QDockWidget.DockWidgetMovable)
            self.addDockWidget(Qt.BottomDockWidgetArea, self.slider_dock)

        # set playback speed
        try:
            self._timer.fps = self.reader.frame_rate
        except (AttributeError, KeyError):
            self._timer.fps = 25.

        self.update_display()
        self.resize_display()

    def update_display(self, display_class=None):
        """Change display mode."""
        if display_class is None:
            display_class = Display

        shape = [self.reader.sizes['y'], self.reader.sizes['x']]
        if display_class.ndim == 3:
            try:
                shape = [self.reader.sizes['z']] + shape
            except KeyError:
                raise KeyError('z axis does not exist: cannot display in 3D')

        if self._display is not None:
            self._display.close()
        self._display = display_class(self, shape)

        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Expanding,
                                  QtWidgets.QSizePolicy.Expanding)
        self.canvas.updateGeometry()
        self.main_layout.addWidget(self.canvas, 0, 0)
        self.canvas.keyPressEvent = self.keyPressEvent
        self.update_original_image()

    def update_original_image(self):
        """Update the original image that is being viewed."""
        if self._display.ndim == 3 and 'z' not in self.reader.sizes:
            raise ValueError('z axis does not exist: cannot display in 3D')
        if self.is_multichannel and 'c' not in self.reader.sizes:
            raise ValueError('c axis does not exist: cannot display multicolor')

        # Make sure that the reader bundle_axes settings are correct
        bundle_axes = ''
        if self.is_multichannel:
            bundle_axes += 'c'
        if self._display.ndim == 3:
            bundle_axes += 'z'
        self.reader.bundle_axes = bundle_axes + 'yx'

        # Update slider positions
        for name in self.sliders:
            self.sliders[name].val = self._index[name]

        # Update image
        self.reader.default_coords.update(self._index)
        image = self.reader[self._index['t']]

        if len(self._images) == 0:
            self._images = [image] + [None] * len(self.plugins)
        else:
            self._images[0] = image

        self.update_processed_image()

    def update_processed_image(self, plugin=None):
        """Update the processing function stack starting from `plugin`."""
        if self.original_image is None:
            return

        if plugin is None:
            first_plugin = 0
        else:
            first_plugin = self.plugins.index(plugin)

        # reset the image stack if necessary
        required_len = len(self.plugins) + 1
        if len(self._images) != required_len:
            first_plugin = 0  # we will need to reform the entire stack
            self._images = [self.original_image] + [None] * (required_len - 1)

        for i, p in enumerate(self.plugins[first_plugin:], start=first_plugin):
            processed = p.process_image(self._images[i])
            if processed is None:
                processed = self._images[i]
            self._images[i + 1] = processed
        self.update_view()

    def update_view(self):
        """Emit processed image to display."""
        if self.image is None:
            return

        self._display.update_image(to_rgb_uint8(self.image,
                                                autoscale=self.autoscale))
        self.original_image_changed.emit()

    @property
    def original_image(self):
        """The original image"""
        if len(self._images) == 0:
            return
        return self._images[0]

    @property
    def image(self):
        """The image that is being displayed"""
        if len(self._images) == 0:
            return
        return self._images[-1]

    @property
    def canvas(self):
        return self._display.canvas

    @property
    def ax(self):
        return self._display.ax

    @property
    def fig(self):
        return self._display.fig

    # Change the current index

    @property
    def index(self):
        """The current index (dictionary). Setting this has no effect."""
        return self._index.copy()  # copy the dict to make it read only

    def _set_index(self, value, name):
        """Set the index without checks. Mainly for timer callback."""
        try:
            if self._index[name] == value:
                return  # do nothing when no coordinate was changed
        except KeyError:
            pass  # but continue when a coordinate did not exist
        self._index[name] = value
        self.update_original_image()

    def set_index(self, value=0, name='t'):
        """Update the index along a specific axis"""
        if name not in self.reader.sizes:
            return ValueError("Axis '{}' not in reader".format(name))
        # clip value if necessary
        if value < 0:
            value = 0
        elif value >= self.reader.sizes[name]:
            value = self.reader.sizes[name] - 1
        if self.is_playing and name == 't':
            self._timer.reset(value)
        self._set_index(value, name)

    def channel_tab_callback(self, index):
        """Callback function for channel tabs."""
        if index == 0 and self.is_multichannel:
            return  # do nothing: already multichannel
        elif not self.is_multichannel and (self._index['c'] == index - 1):
            return  # do nothing: correct monochannel
        self.is_multichannel = index == 0
        if index > 0:  # monochannel: update channel field
            self._index['c'] = index - 1  # because 0 is multichannel
        self.update_original_image()

    # Access to the reader and its properties

    @property
    def sizes(self):
        return self.reader.sizes.copy()

    @property
    def autoscale(self):
        return self._autoscale.isChecked()

    @autoscale.setter
    def autoscale(self, value):
        return self._autoscale.setChecked(value)

    def close_reader(self):
        """Close the current reader"""
        if self.reader is None:
            return
        if self.is_playing:
            self.stop()
        if self.slider_dock is not None:
            self.slider_dock.close()
        if self.channel_tabs is not None:
            self.channel_tabs.close()
        self.reader.close()
        self.reader = None
        self._display.close()

    # Video playback

    def play_callback(self, name, value):
        """Callback function for play checkbox."""
        if value == self.is_playing:
            return
        if value:
            self.play()
        else:
            self.stop()

    def play(self, start=True, fps=None):
        """Control movie playback."""
        if self._play_checkbox is not None:
            self._play_checkbox.val = start
        if start == self.is_playing:
            return
        if start:
            self._timer.start(self._index['t'], self.reader.sizes['t'])
            self._timer.next_frame.connect(lambda x: self._set_index(x, 't'))
            if fps is not None:
                self.fps = fps
        else:
            self._timer.stop()
        self.is_playing = start

    @property
    def fps(self):
        return self._timer.fps

    @fps.setter
    def fps(self, value):
        if self.is_playing:
            self._timer.fps = value

    def stop(self):
        """Stop the movie."""
        self.play(False)

    # File drag & drop

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            links = []
            for url in event.mimeData().urls():
                links.append(str(url.toLocalFile()))
            self._dropped.emit(links)
        else:
            event.ignore()

    def _open_dropped(self, links):
        for fn in links:
            if os.path.exists(fn):
                self.open_file(fn)
                break

    # Handling user input

    def resize_display(self, w=None, h=None, factor=1):
        """Resize the image display widget to a certain size or by a factor."""
        h_im, w_im = self.sizes['y'], self.sizes['x']
        h_im *= factor
        w_im *= factor
        if h is None and w is None:
            h = h_im
            w = w_im
        elif h is None:
            h = int(w * h_im / w_im)
        elif w is None:
            w = int(h * w_im / h_im)
        self.showNormal()  # make sure not to be in maximized mode
        self._display.resize(w, h)

    def keyPressEvent(self, event):
        if type(event) == QtGui.QKeyEvent:
            key = event.key()
            modifiers = event.modifiers()
            if key in range(0x30, 0x39 + 1):  # number keys: move to deciles
                index = int(self.reader.sizes['t'] * (key - 48) / 10)
                self.set_index(index, 't')
            if key in range(0x01000037,  # F8-F12 keys: change channel
                            0x0100003b + 1) and 'c' in self.reader.sizes:
                index = key - 0x01000037
                print('key pressed to {}'.format(index))
                if index <= self.reader.sizes['c']:
                    self.channel_tabs.setCurrentIndex(index)
            if key in [QtCore.Qt.Key_N, QtCore.Qt.Key_Right]:
                if modifiers == Qt.NoModifier:
                    jump = 1
                elif modifiers == Qt.ShiftModifier:
                    jump = 10
                elif modifiers == Qt.ControlModifier:
                    jump = 25
                elif modifiers == (Qt.ShiftModifier | Qt.ControlModifier):
                    jump = 100
                else:
                    jump = 0
                self.set_index(self._index['t'] + jump)
                event.accept()
            elif key in [Qt.Key_P, Qt.Key_Left]:
                if modifiers == Qt.NoModifier:
                    jump = 1
                elif modifiers == Qt.ShiftModifier:
                    jump = 10
                elif modifiers == Qt.ControlModifier:
                    jump = 25
                elif modifiers == (Qt.ShiftModifier | Qt.ControlModifier):
                    jump = 100
                else:
                    jump = 0
                self.set_index(self._index['t'] - jump)
                event.accept()
            elif key == Qt.Key_R:
                index = np.random.randint(0, self.reader.sizes['t'] - 1)
                self.set_index(index, 't')
                event.accept()
            elif key == Qt.Key_Space:
                self.play(not self.is_playing)
                event.accept()
            elif key == Qt.Key_BracketRight:
                self.fps *= 1.2
            elif key == Qt.Key_BracketLeft:
                self.fps *= 0.8
            elif key == Qt.Key_Backslash:
                self.fps *= -1
            elif key == Qt.Key_Equal:
                try:
                    self.fps = self.reader.frame_rate
                except AttributeError:
                    self.fps = 25.
            elif key == Qt.Key_F:
                self._display.set_fullscreen()
            elif key == Qt.Key_Escape:
                self._display.set_fullscreen(False)
            elif key == Qt.Key_Plus:
                if hasattr(self.renderer, 'zoom'):
                    self._display.zoom(1)
            elif key == Qt.Key_Minus:
                if hasattr(self.renderer, 'zoom'):
                    self._display.zoom(-1)
            elif key == Qt.Key_R:
                if hasattr(self.renderer, 'zoom'):
                    self._display.zoom()
            elif key == Qt.Key_Z:
                self.undo.emit()
            elif key == Qt.Key_Y:
                self.redo.emit()
            elif key == Qt.Key_A:
                self.resize_display(factor=1 / 2)
            elif key == Qt.Key_S:
                self.resize_display(factor=1)
            elif key == Qt.Key_D:
                self.resize_display(factor=2)
            else:
                event.ignore()
        else:
            event.ignore()

    @property
    def status(self):
        return None

    @status.setter
    def status(self, value):
        self._status_bar.showMessage(str(value))

    # # Output data (EXPERIMENTAL)
    #
    def to_pixmap(self):
        pixmap = QtWidgets.QPixmap(self.canvas.size())
        self.canvas.render(pixmap)
        return pixmap

    def to_clipboard(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setPixmap(self.to_pixmap())

    @staticmethod
    @memoize
    def _get_all_files_in_dir(directory):
        return sorted([f for f in listdir(directory) if isfile(join(directory, f))], key=natural_keys)

    #
    # def to_frame(self):
    #     return Frame(rgb_view(self.to_pixmap().toImage()),
    #                  frame_no=self.index['t'])
    #
    # def save_file(self, filename=None):
    #     str_filter = ";;".join(['All files (*.*)',
    #                             'H264 video (*.avi)',
    #                             'MPEG4 video (*.mp4 *.mov)',
    #                             'Windows Media Player video (*.wmv)'])
    #
    #
    #     if VideoClip is None:
    #         raise ImportError('The MoviePy exporter requires moviepy to work.')
    #
    #     if filename is None:
    #         try:
    #             cur_dir = os.path.dirname(self.reader.filename)
    #         except AttributeError:
    #             cur_dir = ''
    #         filename = QtWidgets.QFileDialog.getSaveFileName(self,
    #                                                          "Export Movie",
    #                                                          cur_dir,
    #                                                          str_filter)
    #         if isinstance(filename, tuple):
    #             # Handle discrepancy between PyQt4 and PySide APIs.
    #             filename = filename[0]
    #
    #     _, ext = os.path.splitext(os.path.basename(filename))
    #     ext = ext[1:].lower()
    #     if ext == 'wmv':
    #         codec = 'wmv2'
    #     else:
    #         codec = None  # let moviepy decide
    #     if ext == '':
    #         filename += '.mp4'
    #
    #     try:
    #         rate = self.reader.frame_rate
    #     except AttributeError:
    #         rate = 25
    #
    #     self.reader.iter_axes = ['t']
    #     self.status = 'Saving to {}'.format(filename)
    #     pims.export(self.reader, filename, rate, codec=codec)
    #     self.update_image()
    #     self.status = 'Done saving {}'.format(filename)
