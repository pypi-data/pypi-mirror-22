# encoding: utf-8
# author: WU Dingcheng

from __future__ import absolute_import
from matplotlib.dates import num2date
from matplotlib.patches import Rectangle
from numpy import nan

# from PyQt4.QtCore import pyqtSlot
# from PyQt4.QtGui import (QApplication, QDesktopWidget, QDialog, QFileDialog,
#                          QIcon, QMainWindow, QMessageBox, QPixmap)
from qtpy.QtCore import Slot
from qtpy.QtGui import QIcon, QPixmap, QTextCursor
from qtpy.QtWidgets import (QApplication, QDesktopWidget, QDialog,
                            QMainWindow, QMessageBox, QFileDialog)
from qtpy.compat import getopenfilenames, getopenfilename

from .TSModel import *
from .TSThread import *
from .TSWidgets import *
from qtpy.uic import loadUiType


class TSAboutDialog(QDialog, AboutDialog):
    def __init__(self):
        super(TSAboutDialog, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("TSAnalyzer - About")
        self.setWindowIcon(QIcon(":/TSResource/images/icon.ico"))
        pix = QPixmap(':/TSResource/images/icon.png')
        self.imgLabel.setPixmap(pix)


class MainWindow(QMainWindow, MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # self.dialog = QFileDialog(self)
        # self.dialog.setFileMode(QFileDialog.ExistingFile)
        self.setWindowTitle("TSAnalyzer")
        self.site = None
        self._filename = None
        self.df = None
        self.df_fit = None
        self.df_residual = None
        self.df_continuous = None
        self.column_names = None
        # self._offsets = None
        self.offsets_file = None
        self.offsets = {}
        self.offsets_plots = {}
        self.rects = {}
        self.error_curves = []
        self.fit_lines = []
        self.tsPlotWidget = matplotlibwidget.MatplotlibWidget()
        self.spPlotWidget = matplotlibwidget.MatplotlibWidget()
        self.tab.layout().addWidget(self.tsPlotWidget)
        self.tab2.layout().addWidget(self.spPlotWidget)
        self.ts_figure = self.tsPlotWidget.figure
        self.sp_figure = self.spPlotWidget.figure
        self.tsfit_thread = None
        self.ts_reader = TSReader()
        self.ts_reader.outlierEndSignal.connect(self._outliers_end)
        self.ts_reader.fitEndSignal.connect(self._detrend_end)
        self.plotTSThread = TSPlotThread(self.ts_figure)
        self.plotTSThread.plotBreaksEnd.connect(self._plot_breaks_end)
        self.spectralThread = TSSpectralThread(self.sp_figure)
        self.tsToolBar = TSToolBar(self.ts_figure.canvas, None)
        self.spToolBar = SPToolBar(self.sp_figure.canvas, None)
        self.toolbar_dicts = {1: self.tsToolBar,
                              2: self.spToolBar}
        # for widget in (self.tsPlotWidget, self.spPlotWidget):
        #     widget.figure.subplots_adjust(left=0.1,
        #                                   right=0.90,
        #                                   top=0.95,
        #                                   bottom=0.05,
        #                                   wspace=0.0,
        #                                   hspace=0.05)
        #     widget.figure.set_facecolor((1, 1, 1, 0))
        # self.ts_figure.delaxes(self.ts_figure.get_axes()[0])
        # self.ts_figure.canvas.draw()
        # self.sp_figure.delaxes(self.sp_figure.get_axes()[0])
        # self.sp_figure.canvas.draw()
        for index, toolbar in self.toolbar_dicts.items():
            self.addToolBar(toolbar)
            toolbar.setVisible(index == 1)

        self.sigsegDialog = TSSigsegDialog(parent=self)
        self.sigsegThread = TSSigsegThread(self.sigsegDialog.figure)
        self.sigsegThread.sigsegEndSignal.connect(self._sigseg_end)
        self.sigsegDialog.addOffsetsSignal.connect(self._add_offsets)
        self.alphaLineEdit.setFixedWidth(self.alphaLineEdit.width())
        self.betaLineEdit.setFixedWidth(self.alphaLineEdit.width())
        self.muLineEdit.setFixedWidth(self.alphaLineEdit.width())
        self.epsLineEdit.setFixedWidth(self.alphaLineEdit.width())
        self.lamepsLineEdit.setFixedWidth(self.alphaLineEdit.width())
        self.tolEdit.setFixedWidth(self.alphaLineEdit.width())
        self.iterEdit.setFixedWidth(self.alphaLineEdit.width())
        self.toolBox.setItemEnabled(0, False)
        self.msRadio.setEnabled(False)
        self.betaWidget.setVisible(False)
        self.gammaWidget.setVisible(False)
        self._init_style()
        self._init_signals()

    def _init_style(self):
        from .style import font_style
        self.setStyleSheet(font_style)

        self.setWindowIcon(QIcon(":/TSResource/images/icon.png"))
        self.addFilesButton.setIcon(QIcon(":/TSResource/images/add.png"))
        self.addFilesButton.setToolTip("Add time series files")
        self.addOffsetButton.setIcon(QIcon(":/TSResource/images/offset.png"))
        self.addOffsetButton.setToolTip("Add offsets file")
        self.actionHeader.setIcon(QIcon(":/TSResource/images/editor.png"))
        self.actionDate.setIcon(QIcon(":/TSResource/images/calendar.png"))
        self.actionAbout.setIcon(QIcon(":/TSResource/images/about.png"))
        self.actionHelp.setIcon(QIcon(":/TSResource/images/help.png"))
        self.actionOpen.setIcon(QIcon(":/TSResource/images/add.png"))
        self.actionFigure.setIcon(QIcon(":/TSResource/images/save.png"))
        self.actionDetrend.setIcon(QIcon(":/TSResource/images/batch.png"))
        self.deleteOffsetButton.setIcon(
            QIcon(":/TSResource/images/delete.png"))
        self._update_data_combox()
        self.filesListWidget.setToolTip(
            "Double click to load the selected file")
        self.deleteOffsetButton.setToolTip("Remove the offsets file")

    def _init_signals(self):
        self.toolBox.currentChanged.connect(self._toolBox_changed)
        self.tabWidget.currentChanged.connect(self._tabWidget_changed)

        self.addFilesButton.clicked.connect(self._click_addFilesButton)
        self.filesListWidget.doubleClicked.connect(self._dbclick_listwidget)
        self.prevButton.clicked.connect(
            lambda: self._click_prevOrNextButton(-1))
        self.nextButton.clicked.connect(
            lambda: self._click_prevOrNextButton(1))
        self.tsToolBar.BreakLineDrawEndSignal.connect(self._ts_new_range)
        self.tsToolBar.RangeDrawEndSignal.connect(self._ts_new_range)

        self.addOffsetButton.clicked.connect(self._click_addOffsetButton)
        self.outliersButton.clicked.connect(self._click_outliersButton)
        self.detrendButton.clicked.connect(self._click_detrendButton)
        self.offsetsListWidget.doubleClicked.connect(
            self._dbclick_offsetsListWidget)
        # spectral slots
        self.spAnalysisButton.clicked.connect(self._click_spAnalysisButton)
        self.fftWidget.setVisible(False)
        self.spMethodBox.currentIndexChanged.connect(
            lambda i=self.spMethodBox.currentText(): self.fftWidget.setVisible(int(i) == 1))
        self.writeOffsetsButton.clicked.connect(self._click_writeOffsetsButton)
        self.saveButton.clicked.connect(self._click_saveButton)
        self.deleteButton.clicked.connect(self._click_deleteButton)
        self.plotTSThread.plotEndSignal.connect(self.display_information)

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = "%s" % filename
        self.df = None
        self.df_fit = None
        self.df_residual = None
        self.load_filename()

    def load_filename(self):
        if self.filename:
            # self.df = readtsfile(self.filename)
            self.ts_reader.read_file(self.filename)
            if self.ts_reader.df is None:
                QMessageBox.critical(self, "Unsupport Formats", 'cannot read %s' % self.filename,
                                     QMessageBox.Ok)
                self._filename = None
                return
            self.df = self.ts_reader.df
            self.column_names = self.ts_reader.columns
            self.site = self.ts_reader.name
            self.unit = self.ts_reader.unit
            self.time_unit = self.ts_reader.time_unit
            self.periodUnitLabel.setText(self.time_unit)
            self.sigmaUintLabel.setText((self.unit))
            self.ts_figure.clear()
            self.sp_figure.clear()
            self.offsetStationLabel.setText(self.site)
            self.tabWidget.setCurrentIndex(0)
            # self.offsets[self.site.lower()] = {}
            self.offsets_plots = {}
            self.offsetsListWidget.clear()
            for action in self.tsToolBar.actions:
                if action is not None and action.isChecked():
                    action.trigger()
            if self.offsets_file:
                offsets = get_offsets(
                    self.site.lower(), file=self.offsets_file)
                if offsets is None:
                    self.plotTSThread.plot(self.df, unit=self.unit,
                                           errorbar=self.tsToolBar.errorbarAction.isChecked(),
                                           title=self.site, cols=self.column_names, task='ts')
                self._add_offsets(offsets)
            else:
                self.plotTSThread.plot(self.df, unit=self.unit,
                                       errorbar=self.tsToolBar.errorbarAction.isChecked(),
                                       title=self.site, cols=self.column_names, task='ts',
                                       offsets=self.offsets.get(self.site.lower(), None))
            self._update_data_combox()
            self._display_statistics()
            self.display_information("load %s" % self.filename)

    @Slot()
    def on_actionHeader_triggered(self):
        self.headerDialog = TSHeaderDialog(self)
        for index in xrange(self.filesListWidget.count()):
            item = self.filesListWidget.item(index)
            self.headerDialog.filesListWidget.addItem(item)
        self.headerDialog.show()

    @Slot()
    def on_actionDate_triggered(self):
        self.dateWidget = TSDateWidget(self)
        self.dateWidget.show()

    def _add_offsets(self, offset):
        if offset is None:
            return
        if self.site.lower() not in self.offsets:
            self.offsets[self.site.lower()] = {}
        for date_str, components in offset.items():
            if date_str not in self.offsets[self.site.lower()]:
                self.offsets[self.site.lower()][date_str] = components
            else:
                self.offsets[self.site.lower()][date_str].update(components)

        self.plotTSThread.plot(self.df, unit=self.unit,
                               errorbar=self.tsToolBar.errorbarAction.isChecked(),
                               title=self.site, cols=self.column_names, task='ts',
                               offsets=self.offsets[self.site.lower()])
        self.offsetsListWidget.clear()
        self.offsetsListWidget.addItems(
            offset_to_list(self.offsets[self.site.lower()]))

    def _dbclick_listwidget(self):
        if self.filesListWidget.currentItem() is not None:
            filename = self.filesListWidget.currentItem().text()
            self.filename = "%s" % filename

    def _dbclick_offsetsListWidget(self):
        item = str(self.offsetsListWidget.currentItem().text())
        temp = item.split()
        date = temp[0]
        col = temp[1]
        if len(temp) == 5:
            breaks = ' '.join(temp[2:4])
            tau = int(temp[4])
        else:
            breaks = temp[2]
            tau = 0
        self.offsetDialog = TSOffsetDialog(
            parent=self, date=date, col=col, breaks=breaks, tau=tau)
        self.offsetDialog.JUMP_EDITOR_DELETE.connect(self.edit_offset_callback)
        self.offsetDialog.JUMP_EDITOR_DONE.connect(self.edit_offset_callback)
        self.offsetDialog.show()

    def edit_offset_callback(self, obj):
        orign = obj['orign']
        col = obj['col']
        try:
            patch = self.offsets_plots[orign][col]
            patch.remove()
        except:
            pass
        if not obj['delete']:
            self.offsets[self.site.lower()][orign].pop(col)
            self._add_offsets(obj['edit'])
        else:
            self.ts_figure.canvas.draw_idle()
            self.offsets_plots[orign].pop(col)
            self.offsets[self.site.lower()][orign].pop(col)
            self.offsetsListWidget.clear()
            self.offsetsListWidget.addItems(
                offset_to_list(self.offsets[self.site.lower()]))

    @Slot()
    def on_actionAbout_triggered(self):
        self.aboutDialog = TSAboutDialog()
        self.aboutDialog.show()

    def _click_addFilesButton(self):
        # dialog = QFileDialog(self)
        files = getopenfilenames(self,
                                 "Choose Time Series Files",
                                 '',
                                 self.tr('tseries (*.dat *.neu *.tseries *.pos)'),
                                 None,
                                 QFileDialog.DontUseNativeDialog)[0]
        self._add_files_to_fileListWidget(files)

    def _add_files_to_fileListWidget(self, files):
        # files = [i for i in files]
        items = []
        for index in range(self.filesListWidget.count()):
            items.append(self.filesListWidget.item(index).text())
        items = list(set(items + list(files)))
        self.filesListWidget.clear()
        self.filesListWidget.addItems(items)

    def _click_addOffsetButton(self):
        # dialog = QFileDialog(self)
        filename = getopenfilename(self,
                                   'Choose Offsets file',
                                   '',
                                   self.tr('*.json'),
                                   None,
                                   QFileDialog.DontUseNativeDialog)[0]
        filename = u"%s" % filename
        if filename:
            self.offsetEdit.setText(filename)
            if self.site:
                offset = get_offsets(self.site.lower(), file=filename)
                self._add_offsets(offset)
            self.offsets_file = filename

    def _click_deleteButton(self):
        item = self.filesListWidget.currentRow()
        self.filesListWidget.takeItem(item)
        if len(self.filesListWidget.selectedItems()) == 0:
            self.ts_figure.clear()
            self.ts_figure.canvas.draw_idle()
            self.sp_figure.clear()
            self.sp_figure.canvas.draw_idle()
            self.df = None

    def _click_saveButton(self):
        data = str(self.tsDataBox.currentText())
        if data == 'Original Data':
            df = self.df
        if data == 'Fit Data':
            df = self.df_fit
        if data == 'Residuals':
            df = self.df_residual
        if data == 'Continuous':
            df = self.df_continuous
        # filename = self.dialog.getSaveFileName(self, 'Save Data',
        #                                        '%s.neu' % self.site, 'neu',
        #                                        None, QFileDialog.DontUseNativeDialog)
        # filename = "%s" % filename
        filename = getsavefilename(
            self,
            'Save Data',
            '%s.neu' % self.site,
            'neu',
            None,
            QFileDialog.DontUseNativeDialog)[0]
        if filename:
            self.ts_reader.write(df, filename)
            self.display_information(
                "Write %s to %s successfully" % (data, filename))

    def _click_writeOffsetsButton(self):
        if len(self.offsets.keys()) == 0:
            return
        if self.offsets_file is not None:
            reply = QMessageBox.question(self,
                                         'Writing Offsets',
                                         "Write to existing %s" % self.offsets_file,
                                         QMessageBox.Yes,
                                         QMessageBox.No)
            if reply == QMessageBox.Yes:
                saved_filename = self.offsets_file
            else:
                saved_filename = getsavefilename(self,
                                                 'Save Offsets',
                                                 'offsets.json',
                                                 '*.json')[0]
        else:
            saved_filename = getsavefilename(self,
                                             'Save Offsets',
                                             'offsets.json',
                                             '*.json',
                                             None,
                                             QFileDialog.DontUseNativeDialog)[0]
            saved_filename = "%s" % saved_filename
        if saved_filename:
            write_offsets(self.offsets, file=saved_filename)

    def _display_statistics(self):
        if self.df is not None:
            self.statisticsEdit.clear()
            ds = self.df.describe()
            infos = ['std', 'mean']
            s = self.site.upper()
            s += ' period:\n%s to %s\n' % (
                self.df.index[0].strftime('%Y-%m-%d'),
                self.df.index[-1].strftime('%Y-%m-%d'))
            count = self.df.ix[:, 1].count()
            s += '{} epochs   '.format(count)
            s += 'gap: {:.1%}\n'.format(
                1 - 1.0 * count / (self.df.index[-1] - self.df.index[0]).days)
            for i in self.column_names:
                s += i.upper() + ':\n'
                for info in infos:
                    s += '%s: %8.2f\t' % (info, ds[i][info])
                s += '\n'
            self.statisticsEdit.appendPlainText(s)

    def _plot_breaks_end(self, plot):
        try:
            self.offsets_plots.update(plot)
        except:
            self.offsets_plots = plot

    def _update_data_combox(self):
        data = []
        if self.df is not None:
            data.append('Original Data')
        if self.df_fit is not None:
            data.append('Fit Data')
        if self.df_residual is not None:
            data.append('Residuals')
        if self.df_continuous is not None:
            data.append('Continuous')
        if len(data) == 0:
            self.tsDataBox.setVisible(False)
            self.spDataBox.setEnabled(False)
            self.saveButton.setVisible(False)
        else:
            self.tsDataBox.clear()
            self.spDataBox.clear()
            self.tsDataBox.addItems(data)
            self.spDataBox.addItems(data)
            self.tsDataBox.setVisible(True)
            self.saveButton.setVisible(True)
            self.spDataBox.setEnabled(True)

    def _get_analysis_paramenters(self):
        paramenters = None
        try:
            polys = int(self.polyBox.value())
            periods = list(map(float, str(self.periodEdit.text()).split()))
            sigma = list(map(float, str(self.sigmaEdit.text()).split()))
            iqr_factor = int(self.iqrFactorBox.value())
            iqr_window = int(self.iqrWindowBox.value())
            paramenters = {'polys': polys, 'periods': periods,
                           'offsets': self.offsets.get(self.site.lower(), None),
                           'sigma': sigma, 'iqr_factor': iqr_factor, 'iqr_window': iqr_window}

        except Exception as ex:
            QMessageBox.critical(self, "Error Input", str(ex),
                                 QMessageBox.Ok)
        return paramenters

    def _click_outliersButton(self):
        if self.df is None:
            return
        paramenters = self._get_analysis_paramenters()
        if paramenters is None:
            return
        paramenters['task'] = 'outliers'
        self.ts_reader.render(**paramenters)

    def _outliers_end(self, outlier_dict):
        sigma = outlier_dict.get('sigma', None)
        iqr = outlier_dict.get('iqr', None)
        if sigma is not None:
            self.df.ix[sigma] = nan
        if iqr is not None:
            self.df.ix[iqr] = nan
        self.offsets_plots = {}
        self.plotTSThread.plot(self.df, unit=self.unit,
                               errorbar=self.tsToolBar.errorbarAction.isChecked(),
                               title=self.site, cols=self.column_names, task='ts',
                               offsets=self.offsets.get(self.site.lower(), None))
        self._display_statistics()
        self._update_data_combox()

    def _click_detrendButton(self):
        if self.df is None:
            return
        paramenters = self._get_analysis_paramenters()
        if paramenters is None:
            return
        paramenters['task'] = 'detrend'
        if self.df is not None:
            self.detrendButton.setEnabled(False)
            paramenters.update({'cols': self.column_names})
            try:
                self.ts_reader.render(**paramenters)
            except Exception as ex:
                QMessageBox.critical(self, "Error Detrending", str(ex),
                                     QMessageBox.Ok)
                self.detrendButton.setEnabled(True)

    def _detrend_end(self, result):
        self.detrendButton.setEnabled(True)
        self.df_fit = result['fit']
        self.df_residual = result['residual']
        self.df_continuous = result['continuous']
        if self.actionDetrendLog.isChecked():
            pos = self.frameGeometry().topRight()
            x = pos.x()
            y = pos.y()
            rect = QDesktopWidget().screenGeometry()
            if x + 10 > rect.width():
                x -= 320
                y += 30
            else:
                y += 20
                x += 20
            self.logDialog = TSLogDialog(
                parent=self, name=self.site, log=result['log'])
            self.logDialog.setGeometry(x, y,
                                       300, self.frameGeometry().height() - 20)
            self.logDialog.show()
        else:
            log = result['log']
            self.display_information(log)
        self.detrend_plot_check()
        self._update_data_combox()

    @Slot(name="on_noOffsetsRadio_clicked")
    @Slot(name='on_fitCheck_clicked')
    @Slot(name='on_residualCheck_clicked')
    def detrend_plot_check(self):
        if self.fitCheck.isChecked() and self.df_fit is not None:
            self.plotTSThread.plot(self.df, unit=self.unit,
                                   errorbar=self.tsToolBar.errorbarAction.isChecked(),
                                   title="%s Fit" % self.site, cols=self.column_names,
                                   task='ts', fit=self.df_fit,
                                   offsets=self.offsets.get(self.site.lower(), None))
            self.offsets_plots = {}
        if self.residualCheck.isChecked() and self.df_residual is not None:
            self.plotTSThread.plot(self.df_residual, unit=self.unit,
                                   errorbar=self.tsToolBar.errorbarAction.isChecked(),
                                   title="%s Residuals" % self.site, cols=self.column_names,
                                   task='ts')
        if self.noOffsetsRadio.isChecked() and self.df_continuous is not None:
            self.plotTSThread.plot(self.df_continuous, unit=self.unit,
                                   errorbar=self.tsToolBar.errorbarAction.isChecked(),
                                   title="%s Continuous" % self.site, cols=self.column_names,
                                   task='ts')

    def _click_prevOrNextButton(self, ind):
        current_index = self.filesListWidget.currentRow()
        next_index = current_index + ind
        if 0 <= next_index <= self.filesListWidget.count() - 1:
            self.filesListWidget.setCurrentRow(next_index)
            self._dbclick_listwidget()

    def _toolBox_changed(self, index):
        self.tabWidget.setCurrentIndex(index - 1)

    def _tabWidget_changed(self, index):
        index += 1
        self.toolBox.setCurrentIndex(index)
        # print index
        # index = 1 if index <= 1 else index
        toolbar = self.toolbar_dicts[index]
        for key, toolbar in self.toolbar_dicts.items():
            toolbar.setVisible(key == index)

    def _click_logAction(self, flag):
        ax = self.sp_figure.get_axes()[0]
        if flag:
            ax.set_xscale("log", nonposx='clip')
            ax.set_yscale("log", nonposy='clip')
            ax.relim()
        else:
            ax.set_xscale("linear")
            ax.set_yscale("linear")
        self.sp_figure.canvas.draw_idle()

    def _click_spAnalysisButton(self):
        if self.df is None:
            return
        for action in self.spToolBar.actions():
            if action.isChecked():
                action.trigger()
        data = str(self.spDataBox.currentText())
        if data == 'Original Data':
            df = self.df
            title = self.site
        if data == 'Fit Data':
            df = self.df_fit
            title = '%s Fit Spectrum' % self.site
        if data == 'Residuals':
            df = self.df_residual
            title = '%s Residual Spectrum' % self.site
        if self.spMethodBox.currentText() == 'Lomb-Scargle':
            self.spectralThread.lombscargle(
                df, cols=self.column_names, title=title,
                fit=self.spLogFitCheck.isChecked())
        if self.spMethodBox.currentText() == 'Periodogram':
            # df = self.ts_reader.interpolate(df, method='spline')
            window = self.fftWindowBox.currentText()
            self.spectralThread.periodogram(df, window=str(window).lower(),
                                            cols=self.column_names, title=title)

    def _ts_new_range(self, patch):
        offset, date_str, col = self._patch_to_offsets(patch)
        if len(self.column_names) > 1:
            reply = QMessageBox.question(self, 'Adding Offsets',
                                         "Adding to another %d components?" % len(
                                             self.column_names),
                                         QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                for c in self.column_names:
                    if c != col:
                        offset[date_str][c] = offset[date_str][col]

        self._add_offsets(offset)
        self.tsToolBar.cursor_line.remove()
        self.tsToolBar.cursor_line = None
        for action in self.tsToolBar.actions:
            if action is not None and action.isChecked():
                action.trigger()

    def _patch_to_offsets(self, patch):
        ind = self.ts_figure.get_axes().index(patch.axes)
        if isinstance(patch, Rectangle):
            x, width = patch.get_x(), patch.get_width()
            date = num2date(x)
            tau = (num2date(x + width) - date).days
            if patch.get_facecolor() == (1.0, 0.0, 0.0, 0.8):
                kind = 'eq log %d' % tau
            if patch.get_facecolor() == (0.0, 0.0, 1.0, 0.8):
                kind = 'eq exp %d' % tau
        else:
            x = patch.get_xdata()[0]
            if patch.get_color() == 'r':
                kind = 'eq'
            if patch.get_color() == 'b':
                kind = 'ep'
            date = num2date(x)
        date_str = date.strftime("%Y%m%d")
        offset = {date_str: {self.column_names[ind]: kind}}
        patch.remove()
        self.ts_figure.canvas.draw_idle()
        return offset, date_str, self.column_names[ind]

    def display_information(self, s):
        s = '>> (%s) %s' % (str(datetime.now())[:-10], s)
        self.consoleEdit.appendPlainText(s)
        self.consoleEdit.moveCursor(QTextCursor.End)

    @Slot()
    def on_actionFigure_triggered(self):
        self.batchDialog = TSPlotBatchDialog(parent=self)
        self.batchDialog.show()

    @Slot()
    def on_actionDetrend_triggered(self):
        self.batchDetrendDialog = TSAnalysisBatchDialog(parent=self)
        self.batchDetrendDialog.show()

    @Slot()
    def on_deleteOffsetButton_clicked(self):
        self.offsets_file = None
        self.offsetEdit.setText('')
        self.offsets = {}
        self.load_filename()

    @Slot()
    def on_actionHelp_triggered(self):
        import webbrowser
        import os
        webbrowser.open(
            'file://' + os.path.realpath('doc/TSAnalyzer User Manual.html'))

    @Slot()
    def on_diffButton_clicked(self):
        if self.df is None:
            return
        df = self.ts_reader.diff(self.df)
        self.plotTSThread.plot(df, task='ts', cols=self.column_names,
                               unit=self.unit,)

    @Slot()
    def on_cumsumButton_clicked(self):
        if self.df is None:
            return
        df = self.ts_reader.cumsum(self.df)
        self.plotTSThread.plot(df, task='ts', cols=self.column_names,
                               unit=self.unit,)

    @Slot()
    def on_sigsegButton_clicked(self):
        # if self.df is None:
        #     return
        # self.offsetsThread = TSOffsetsThread()
        prm = {"alpha": float(self.alphaLineEdit.text()),
               "beta": float(self.betaLineEdit.text()),
               "epsilon": float(self.epsLineEdit.text()),
               "gamma": float(self.gammaLineEdit.text()),
               "mu_eps": float(self.muLineEdit.text()),
               "lambda_epsilon": float(self.lamepsLineEdit.text()),
               'tol': float(self.tolEdit.value()),
               'mx_iter': int(self.iterEdit.value())}
        # df = self.df.dropna()

        # self.offsetsThread.render(df.r.values, prm)
        self.sigsegDialog.show()
        self.sigsegThread.analysis(self.df.dropna(), self.column_names, prm)

    def _sigseg_end(self, ind):
        self.sigsegDialog.line = ind

    @Slot(bool)
    def on_actionOffsets_triggered(self, flag):
        self.toolBox.setItemEnabled(0, flag)


def main():
    import sys
    app = QApplication(sys.argv)
    m = MainWindow()
    m.show()
    app.exec_()


if __name__ == '__main__':
    main()
