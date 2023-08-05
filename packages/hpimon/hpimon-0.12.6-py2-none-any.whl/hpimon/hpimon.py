# -*- coding: utf-8 -*-
"""

Realtime hpi monitor for Vectorview/TRIUX MEG systems.

@author: jussi (jnu@iki.fi)
"""


import sys
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from pkg_resources import resource_filename
import time
import struct
import FieldTrip
import numpy as np
import scipy.linalg
import os.path as op
import traceback
import socket
from config import cfg, cfg_user
import elekta
from rt_server import start_rt_server, stop_rt_server, rt_server_pid
from utils import rolling_fun_strided
import logging
import argparse

logger = logging.getLogger(__name__)


class statusLight(QtWidgets.QWidget):
    """ Creates a status light of given radius """

    def __init__(self, color, radius):
        super(self.__class__, self).__init__()
        self._color = color
        self.diam = radius * 2
        self.update()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color_):
        """ If the color is different from the current one, set it and
        cause paintEvent to occur """
        if self._color != color_:
            self._color = color_
            self.update()

    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QColor(self.color))
        painter.drawEllipse(0, 0, self.diam, self.diam)
        painter.end()

    def sizeHint(self):
        return QtCore.QSize(self.diam, self.diam)


class HPImon(QtWidgets.QMainWindow):

    # new signals must be defined here
    new_data = pyqtSignal()

    def __init__(self):
        super(self.__class__, self).__init__()
        # hardcoded options
        self.VAR_WINDOW = 50  # window for variance computation (ms)
        self.apptitle = 'hpimon'
        # load user interface made with designer
        uifile = resource_filename(__name__, 'hpimon.ui')
        uic.loadUi(uifile, self)
        self.setWindowTitle(self.apptitle)
        self.timer = QtCore.QTimer()
        try:
            cfg._read_user()
        except IOError:  # probably file not found
            self.message_dialog('Cannot find config file, creating %s '
                                'with default values. Please edit the file '
                                'according to your setup and restart.' %
                                cfg_user)
            cfg.__init__()  # reset to default values
            cfg._write_user()
            sys.exit()
        except (ValueError, SyntaxError):  # broken config
            self.message_dialog('Cannot parse config file %s, please check '
                                'the contents of the file or delete it.' %
                                cfg_user)
            sys.exit()

        """ Parse some options """
        linefreq_, cfreqs_ = elekta.read_collector_config(cfg.hpi.
                                                          collector_config)
        self.linefreq = cfg.hpi.line_freq or linefreq_
        self.cfreqs = cfg.hpi.hpi_freqs or cfreqs_
        if not self.cfreqs:
            self.message_dialog('Cannot detect HPI frequencies and none are '
                                'specified in the config file. Aborting.')
            sys.exit()
        if not self.linefreq:
            self.message_dialog('Cannot detect line frequency and none was '
                                'specified in the config file. Aborting.')
            sys.exit()
        self.ncoils = len(self.cfreqs)
        self.serverp = None

        if cfg.server.server_autostart:
            if not op.isfile(cfg.server.server_path):
                self.message_dialog('Cannot find server binary at %s, please '
                                    'check config.' % cfg.server.server_path)
                sys.exit()
            server_bin = op.split(cfg.server.server_path)[1]
            if rt_server_pid(server_bin):
                self.message_dialog('Realtime server already running. '
                                    'Please kill it first.')
                sys.exit()
            if cfg.server.host == 'localhost':
                logger.debug('starting server')
                self.serverp = start_rt_server(cfg.server.server_path,
                                               cfg.server.server_opts.split())
                if not rt_server_pid(server_bin):
                    self.message_dialog('Could not start realtime server.')
                    sys.exit()
                time.sleep(1)  # give the server a second to get started

        self.init_widgets()
        self.ftclient = FieldTrip.Client()
        try:
            self.ftclient.connect(cfg.server.host, port=cfg.server.port)
        except socket.error:
            self.message_dialog('Cannot connect to the realtime server. '
                                'Possibly a networking problem or you have '
                                'specified a wrong TCP port.')
            stop_rt_server(self.serverp)
            sys.exit()

        """ Poll using timer until header info becomes available """
        self.statusbar.showMessage('Waiting for measurement to start...')
        self.timer.timeout.connect(self.start_if_header)
        self.timer.start(cfg.server.buffer_poll_interval)

    def start_if_header(self):
        """ Start if header info has become available. """
        logger.debug('polling for header info')
        if self.ftclient.getHeader():
            self.start()

    def start(self):
        """ We now have header info and can start running """
        self.timer.stop()
        hdrinfo = self.get_header_info()
        self.sfreq = hdrinfo['sfreq']
        self.ch_labels = hdrinfo['labels']
        self.pick_mag, self.pick_grad = self.get_ch_indices(self.ch_labels)
        self.pick_meg = np.sort(np.concatenate([self.pick_mag,
                                                self.pick_grad]))
        self.nchan = len(self.pick_meg)
        self.grad_labels = np.array(self.ch_labels)[self.pick_grad]
        self.mag_labels = np.array(self.ch_labels)[self.pick_mag]
        self.var_window = int(self.sfreq * self.VAR_WINDOW/1000.)
        logger.debug('variance window %d samples' % self.var_window)
        logger.debug('sampling frequency %.2f Hz' % self.sfreq)
        self.init_glm()
        self.last_sample = self.buffer_last_sample()
        self.new_data.connect(self.update_display)
        # from now on, use the timer for data buffer polling
        self.timer.timeout.disconnect(self.start_if_header)
        self.timer.timeout.connect(self.poll_buffer)
        self.timer.start(cfg.server.buffer_poll_interval)
        self.statusbar.showMessage(self.msg_running())

    def init_widgets(self):
        # create SNR labels and add to grid
        for wnum in range(self.ncoils):
            label = QtWidgets.QLabel()
            label.setText(str(self.cfreqs[wnum]) + ' Hz')
            self.gridLayout_SNR.addWidget(label, wnum, 0)
        # create SNR progress bars dynamically and add to grid
        self.progbars_SNR = list()
        for wnum in range(self.ncoils):
            progbar = QtWidgets.QProgressBar()
            progbar.setMinimum(-100)
            progbar.setMaximum(100)
            progbar.setValue(0)
            progbar.setFormat(u'%v dB')
            progbar.setTextVisible(True)
            sty = '.QProgressBar {%s }' % cfg.display.bar_style
            progbar.setStyleSheet(sty)
            self.gridLayout_SNR.addWidget(progbar, wnum, 1)
            self.progbars_SNR.append(progbar)
        self.progbar_sat = QtWidgets.QProgressBar()
        self.progbar_sat.setMinimum(0)
        self.progbar_sat.setMaximum(cfg.limits.max_sat)
        self.progbar_sat.setValue(0)
        self.progbar_sat.setFormat(u'%v')
        self.progbar_sat.setTextVisible(True)
        sty = '.QProgressBar {%s }' % cfg.display.bar_style
        self.progbar_sat.setStyleSheet(sty)
        self.verticalLayout_sat.addWidget(self.progbar_sat)
        

        # create stylesheets for progress bars, according to goodness of value
        self.progbar_styles = dict()
        for val in ['good', 'ok', 'bad']:
            sty = ('QProgressBar {%s} QProgressBar::chunk { background-color: '
                   '%s; %s }' % (cfg.display.bar_style,
                                 cfg.display.bar_colors[val],
                                 cfg.display.bar_chunk_style))
            self.progbar_styles[val] = sty
        # buttons
        self.btnQuit.clicked.connect(self.close)
        self.btnStop.clicked.connect(self.toggle_timer)
        # status light
        self.statlight = statusLight(cfg.display.bar_colors['good'], 50)
        self.statusLightLayout.addSpacing(25)
        self.statusLightLayout.addWidget(self.statlight, 0,
                                         QtCore.Qt.AlignCenter)
        self.statusLightLayout.addSpacing(25)       

    def toggle_timer(self):
        if self.timer.isActive():
            self.statusbar.showMessage(self.msg_stopped())
            self.btnStop.setText('Start monitoring')
            self.timer.stop()
        else:
            self.statusbar.showMessage(self.msg_running())
            self.btnStop.setText('Stop monitoring')
            self.timer.start()

    def msg_running(self):
        return ('Running [%s], poll every %d ms, window %d ms' %
                (cfg.server.host, cfg.server.buffer_poll_interval,
                 cfg.hpi.win_len))

    def msg_stopped(self):
        return 'Stopped'

    def get_ch_indices(self, labels):
        """ Return indices of magnetometers and gradiometers in the
        FieldTrip data matrix """
        grads, mags = [], []
        for ind, ch in enumerate(labels):
            if ch[:3] == 'MEG':
                if ch[-1] == '1':
                    mags.append(ind)
                elif ch[-1] in ['2', '3']:
                    grads.append(ind)
                else:
                    raise ValueError('Unexpected channel name: ' + ch)
        logger.debug('got %d magnetometers and %d gradiometers' %
                     (len(mags), len(grads)))
        return np.array(mags), np.array(grads)

    def get_header_info(self):
        """ Get misc info from FieldTrip header """
        hdr = self.ftclient.getHeader()
        return {'sfreq': hdr.fSample, 'labels': hdr.labels}

    def buffer_last_sample(self):
        """ Return number of last sample available from server. """
        return self.ftclient.getHeader().nSamples

    def poll_buffer(self):
        """ Emit a signal if new data is available in the buffer. """
        buflast = self.buffer_last_sample()
        # buffer last sample can also decrease (reset) if streaming from file
        if buflast != self.last_sample:
            self.new_data.emit()
            self.last_sample = buflast

    def fetch_buffer(self):
        start = self.last_sample - cfg.hpi.win_len + 1
        stop = self.last_sample
        logger.debug('fetching buffer %d - %d (start at t = %.2f s)'
                     % (start, stop, start / self.sfreq))
        try:
            data = self.ftclient.getData([start, stop])
        except struct.error:  # something wrong with the buffer
            logger.warning('errors with the buffer')
            return None
        if data is None:
            logger.warning('server returned no data')
            return None
        else:
            return data[:, self.pick_meg]

    def init_glm(self):
        """ Build general linear model for amplitude estimation """
        # get some info from fiff
        self.linefreqs = (np.arange(cfg.hpi.nharm+1)+1) * self.linefreq
        # time + dc and slope terms
        t = np.arange(cfg.hpi.win_len) / float(self.sfreq)
        self.model = np.empty((len(t),
                               2+2*(len(self.linefreqs)+len(self.cfreqs))))
        self.model[:, 0] = t
        self.model[:, 1] = np.ones(t.shape)
        # add sine and cosine term for each freq
        allfreqs = np.concatenate([self.linefreqs, self.cfreqs])
        self.model[:, 2::2] = np.cos(2 * np.pi * t[:, np.newaxis] * allfreqs)
        self.model[:, 3::2] = np.sin(2 * np.pi * t[:, np.newaxis] * allfreqs)
        self.inv_model = scipy.linalg.pinv(self.model)

    def compute_snr(self, data):
        coeffs = np.dot(self.inv_model, data)  # nterms * nchan
        coeffs_hpi = coeffs[2+2*len(self.linefreqs):]
        resid_vars = np.var(data - np.dot(self.model, coeffs), 0)
        # get total power by combining sine and cosine terms
        # sinusoidal of amplitude A has power of A**2/2
        hpi_pow = (coeffs_hpi[0::2, :]**2 + coeffs_hpi[1::2, :]**2)/2
        # average across channel types separately
        hpi_pow_grad_avg = hpi_pow[:, self.pick_grad].mean(1)
        # hpi_pow_mag_avg = hpi_pow[:, self.pick_mag].mean(1)
        # divide average HPI power by average variance
        snr_avg_grad = hpi_pow_grad_avg / \
            resid_vars[self.pick_grad].mean()
        # snr_avg_mag = hpi_pow_mag_avg / \
        #    resid_vars[self.pick_mag].mean()
        return 10 * np.log10(snr_avg_grad)

    def update_display(self):
        buf = self.fetch_buffer()
        if buf is not None:
            # update saturation widget
            # for each channel, find window with minimum std deviation
            std = rolling_fun_strided(buf, np.std, self.var_window, axis=0)
            min_std = np.min(std, axis=0)
            grad_sat = min_std[self.pick_grad] <= cfg.limits.grad_min_std
            mag_sat = min_std[self.pick_mag] <= cfg.limits.mag_min_std
            nsat = np.count_nonzero(grad_sat) + np.count_nonzero(mag_sat)
            logger.debug('%d saturated channels' % nsat)
            logger.debug('gradiometers: %s' % self.grad_labels[grad_sat])
            logger.debug('magnetometers: %s' % self.mag_labels[mag_sat])
            if nsat < cfg.limits.n_sat_ok:
                sty = self.progbar_styles['good']
                self.statlight.color = cfg.display.bar_colors['good']
            elif nsat < cfg.limits.n_sat_bad:
                sty = self.progbar_styles['ok']
                self.statlight.color = cfg.display.bar_colors['ok']
            else:
                sty = self.progbar_styles['bad']
                self.statlight.color = cfg.display.bar_colors['bad']
            # cap the value at max_sat, as required by progress bar logic
            nsat_ = min(nsat, cfg.limits.max_sat)
            self.progbar_sat.setValue(nsat_)
            self.progbar_sat.setStyleSheet(sty)
            # update snr widgets
            snr = self.compute_snr(buf)
            for wnum in range(self.ncoils):
                this_snr = int(np.round(snr[wnum]))
                self.progbars_SNR[wnum].setValue(this_snr)
                if this_snr > cfg.limits.snr_ok:
                    sty = self.progbar_styles['good']
                elif this_snr > cfg.limits.snr_bad:
                    sty = self.progbar_styles['ok']
                else:
                    sty = self.progbar_styles['bad']
                self.progbars_SNR[wnum].setStyleSheet(sty)

    def message_dialog(self, msg):
        """ Show message with an 'OK' button. """
        dlg = QtWidgets.QMessageBox()
        dlg.setWindowTitle(self.apptitle)
        dlg.setText(msg)
        dlg.addButton(QtWidgets.QPushButton('Ok'),
                      QtWidgets.QMessageBox.YesRole)
        dlg.exec_()

    def closeEvent(self, event):
        """ Confirm and close application. """
        self.timer.stop()
        # disconnect from server
        if self.ftclient:
            self.ftclient.disconnect()
        stop_rt_server(self.serverp)
        event.accept()


def main():

    parser = argparse.ArgumentParser(description='Continuous HPI monitor')
    parser.add_argument('--debug', help='Enable debug output',
                        action='store_true')
    args = parser.parse_args()

    app = QtWidgets.QApplication(sys.argv)

    # debug to stdout if cmd line switch is set
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    streamhandler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s: %(levelname)s: %(message)s')
    streamhandler.setFormatter(formatter)
    handler = streamhandler if args.debug else logging.NullHandler()
    logger.addHandler(handler)

    hpimon = HPImon()

    def my_excepthook(type, value, tback):
        """ Custom exception handler for fatal (unhandled) exceptions:
        report to user via GUI and terminate. """
        tb_full = u''.join(traceback.format_exception(type, value, tback))
        hpimon.message_dialog('Terminating due to unhandled exception. %s'
                              % tb_full)
        stop_rt_server(hpimon.serverp)
        sys.__excepthook__(type, value, tback)
        app.quit()

    sys.excepthook = my_excepthook
    hpimon.show()
    app.exec_()


if __name__ == '__main__':
    main()
