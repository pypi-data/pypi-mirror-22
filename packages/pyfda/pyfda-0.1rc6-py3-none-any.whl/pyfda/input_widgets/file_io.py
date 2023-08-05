# -*- coding: utf-8 -*-
"""
Widget for exporting / importing and saving / loading filter data

Author: Christian Muenker
"""
from __future__ import print_function, division, unicode_literals, absolute_import
import sys, os, io
import logging
logger = logging.getLogger(__name__)

from ..compat import (QtCore, QFD, Qt,
                      QWidget, QPushButton, QComboBox, QLabel, QFont, QFrame,
                      QVBoxLayout, QHBoxLayout)

import scipy.io
import numpy as np
import datetime


try:
    import cPickle as pickle
except:
    import pickle

try:
    import xlwt
except ImportError:
    XLWT = False
    logger.info("Module xlwt not installed -> no *.xls coefficient export")
else:
    XLWT = True

try:
    import XlsxWriter as xlsx
except ImportError:
    XLSX = False
    logger.info("Module XlsxWriter not installed -> no *.xlsx coefficient export")
else:
    XLSX = True

#try:
#    import xlrd
#except ImportError:
#    XLRD = False
#    logger.info("Module xlrd not installed -> no *.xls coefficient import")
#else:
#    XLRD = True
    

import pyfda.filterbroker as fb # importing filterbroker initializes all its globals
import pyfda.pyfda_rc as rc 
import pyfda.pyfda_fix_lib as fix_lib
from pyfda.pyfda_lib import extract_file_ext

# TODO: Save P/Z as well if possible

class File_IO(QWidget):
    """
    Create the widget for entering exporting / importing / saving / loading data
    """
    
    sigFilterLoaded = QtCore.pyqtSignal() # emitted when filter has been loaded successfully

    def __init__(self, parent):
        super(File_IO, self).__init__(parent)

        self._construct_UI()

    def _construct_UI(self):
        """
        Intitialize the user interface
        -
        """
        # widget / subwindow for parameter selection
        self.butExport = QPushButton("Export Coefficients", self)
        self.butExport.setToolTip("Export Coefficients in various formats.")

        self.butImport = QPushButton("Import Coefficients", self)
        self.butImport.setToolTip("Import Coefficients in various formats.")

        self.butSave = QPushButton("Save Filter", self)
        self.butLoad = QPushButton("Load Filter", self)
        
        lblSeparator = QLabel("CSV-Separator:")
        self.cmbSeparator = QComboBox(self)
        self.cmbSeparator.addItems(['","','";"','<TAB>','<CR>'])
        self.cmbSeparator.setToolTip("Specify separator for number fields.")


        # ============== UI Layout =====================================
        bfont = QFont()
        bfont.setBold(True)
        
        bifont = QFont()
        bifont.setBold(True)
        bifont.setItalic(True)

        ifont = QFont()
        ifont.setItalic(True)

        layVIO = QVBoxLayout()
        layVIO.addWidget(self.butSave) # save filter dict -> various formats
        layVIO.addWidget(self.butLoad) # load filter dict -> various formats
        layVIO.addStretch(1)
        
        layVIO.addWidget(self.butExport) # export coeffs -> various formats
        layVIO.addWidget(self.butImport) # export coeffs -> various formats
        layVIO.addStretch(1)

        layHIO = QHBoxLayout()        
        layHIO.addWidget(lblSeparator)
        layHIO.addWidget(self.cmbSeparator)        
        layVIO.addLayout(layHIO)
        layVIO.addStretch(20)
        

        # This is the top level widget, encompassing the other widgets        
        frmMain = QFrame(self)
        frmMain.setLayout(layVIO)

        layVMain = QVBoxLayout()
        layVMain.setAlignment(Qt.AlignTop)
#        layVMain.addLayout(layVIO)
        layVMain.addWidget(frmMain)        
        layVMain.setContentsMargins(*rc.params['wdg_margins'])

            
        self.setLayout(layVMain)

        #----------------------------------------------------------------------
        # SIGNALS & SLOTs
        #----------------------------------------------------------------------
        self.butExport.clicked.connect(self.export_coeffs)
        self.butImport.clicked.connect(self.import_coeffs)
        self.butSave.clicked.connect(self.save_filter)
        self.butLoad.clicked.connect(self.load_filter)

#------------------------------------------------------------------------------        
    def load_filter(self):
        """
        Load filter from zipped binary numpy array or (c)pickled object to
        filter dictionary and update input and plot widgets
        """
        file_filters = ("Zipped Binary Numpy Array (*.npz);;Pickled (*.pkl)")
        dlg = QFD(self)
        file_name, file_type = dlg.getOpenFileName_(
                caption = "Load filter ", directory = rc.save_dir,
                filter = file_filters)
        file_name = str(file_name) # QString -> str

        for t in extract_file_ext(file_filters): # get a list of file extensions
            if t in str(file_type):
                file_type = t
        
        if file_name != "": # cancelled file operation returns empty string
        
            # strip extension from returned file name (if any) + append file type:
            file_name = os.path.splitext(file_name)[0] + file_type   

            file_type_err = False              
            try:
                with io.open(file_name, 'rb') as f:
                    if file_type == '.npz':
                        # http://stackoverflow.com/questions/22661764/storing-a-dict-with-np-savez-gives-unexpected-result
                        a = np.load(f) # array containing dict, dtype 'object'
                        
                        for key in a:
                            if np.ndim(a[key]) == 0:
                                # scalar objects may be extracted with the item() method
                                fb.fil[0][key] = a[key].item()
                            else:
                                # array objects are converted to list first
                                fb.fil[0][key] = a[key].tolist()
                    elif file_type == '.pkl':
                        if sys.version_info[0] < 3:
                            fb.fil = pickle.load(f)
                        else:
                        # this only works for python >= 3.3
                            fb.fil = pickle.load(f, fix_imports = True, encoding = 'bytes')
                    else:
                        logger.error('Unknown file type "%s"', file_type)
                        file_type_err = True
                    if not file_type_err:
                        logger.info('Loaded filter "%s"', file_name)
                         # emit signal -> InputTabWidgets.load_all:
                        self.sigFilterLoaded.emit()
                        rc.save_dir = os.path.dirname(file_name)
            except IOError as e:
                logger.error("Failed loading %s!\n%s", file_name, e)
            except Exception as e:
                logger.error("Unexpected error:", e)
#------------------------------------------------------------------------------
    def save_filter(self):
        """
        Save filter as zipped binary numpy array or pickle object
        """
        file_filters = ("Zipped Binary Numpy Array (*.npz);;Pickled (*.pkl)")
        dlg = QFD(self)
        # return selected file name (with or without extension) and filter (Linux: full text)
        file_name, file_type = dlg.getSaveFileName_(
                caption = "Save filter as", directory = rc.save_dir,
                filter = file_filters)
        
        file_name = str(file_name)  # QString -> str() needed for Python 2.x
        # Qt5 has QFileDialog.mimeTypeFilters(), but under Qt4 the mime type cannot
        # be extracted reproducibly across file systems, so it is done manually:

        for t in extract_file_ext(file_filters): # get a list of file extensions
            if t in str(file_type):
                file_type = t           # return the last matching extension

        if file_name != "": # cancelled file operation returns empty string 

            # strip extension from returned file name (if any) + append file type:
            file_name = os.path.splitext(file_name)[0] + file_type   
            
            file_type_err = False        
            try:
                with io.open(file_name, 'wb') as f:
                    if file_type == '.npz':
                        np.savez(f, **fb.fil[0])
                    elif file_type == '.pkl':
                        # save as a pickle version compatible with Python 2.x
                        pickle.dump(fb.fil, f, protocol = 2)
                    else:
                        file_type_err = True
                        logger.error('Unknown file type "%s"', file_type)

                    if not file_type_err:
                        logger.info('Filter saved as "%s"', file_name)
                        rc.save_dir = os.path.dirname(file_name) # save new dir
                            
            except IOError as e:
                    logger.error('Failed saving "%s"!\n%s\n', file_name, e)

#------------------------------------------------------------------------------
    def export_coeffs(self):
        """
        Export filter coefficients in various formats - see also
        Summerfield p. 192 ff
        """
        dlg = QFD(self)

        file_filters = ("CSV (*.csv);;Matlab-Workspace (*.mat)"
            ";;Binary Numpy Array (*.npy);;Zipped Binary Numpy Array (*.npz)")

        if fb.fil[0]['ft'] == 'FIR':
            file_filters += ";;Xilinx coefficient format (*.coe)"

        # Add further file types when modules are available:
        if XLWT:
            file_filters += ";;Excel Worksheet (.xls)"
        if XLSX:
            file_filters += ";;Excel 2007 Worksheet (.xlsx)"

        # return selected file name (with or without extension) and filter (Linux: full text)
        file_name, file_type = dlg.getSaveFileName_(
                caption = "Export filter coefficients as", 
                directory = rc.save_dir, filter = file_filters) 
        file_name = str(file_name) # QString -> str needed for Python 2

        for t in extract_file_ext(file_filters): # extract the list of file extensions
            if t in str(file_type):
                file_type = t
       
        if file_name != '': # cancelled file operation returns empty string  
            # strip extension from returned file name (if any) + append file type:
            file_name = os.path.splitext(file_name)[0] +  file_type 
         
            ba = fb.fil[0]['ba']
            file_type_err = False
            try:
                if file_type == '.coe': # text / string format
                    with io.open(file_name, 'w', encoding="utf8") as f:
                        self.save_file_coe(f)
                else: # binary format
                    with io.open(file_name, 'wb') as f: 
                        if file_type == '.mat':   
                            scipy.io.savemat(f, mdict={'ba':fb.fil[0]['ba']})
                        elif file_type == '.csv':
                            np.savetxt(f, ba, delimiter = ', ')
                            # newline='\n', header='', footer='', comments='# ', fmt='%.18e'
                        elif file_type == '.npy':
                            # can only store one array in the file:
                            np.save(f, ba)
                        elif file_type == '.npz':
                            # would be possible to store multiple arrays in the file
                            np.savez(f, ba = ba)
                        elif file_type == '.xls':
                            # see
                            # http://www.dev-explorer.com/articles/excel-spreadsheets-and-python
                            # https://github.com/python-excel/xlwt/blob/master/xlwt/examples/num_formats.py
                            # http://reliablybroken.com/b/2011/07/styling-your-excel-data-with-xlwt/
                            workbook = xlwt.Workbook(encoding="utf-8")
                            worksheet = workbook.add_sheet("Python Sheet 1")
                            bold = xlwt.easyxf('font: bold 1')
                            worksheet.write(0, 0, 'b', bold)
                            worksheet.write(0, 1, 'a', bold)
                            for col in range(2):
                                for row in range(np.shape(ba)[1]):
                                    worksheet.write(row+1, col, ba[col][row]) # vertical
                            workbook.save(f)
                
                        elif file_type == '.xlsx':
                            # from https://pypi.python.org/pypi/XlsxWriter
                            # Create an new Excel file and add a worksheet.
                            workbook = xlsx.Workbook(f)
                            worksheet = workbook.add_worksheet()
                            # Widen the first column to make the text clearer.
                            worksheet.set_column('A:A', 20)
                            # Add a bold format to use to highlight cells.
                            bold = workbook.add_format({'bold': True})
                            # Write labels with formatting.
                            worksheet.write('A1', 'b', bold)
                            worksheet.write('B1', 'a', bold)
                
                            # Write some numbers, with row/column notation.
                            for col in range(2):
                                for row in range(np.shape(ba)[1]):
                                    worksheet.write(row+1, col, ba[col][row]) # vertical
                #                    worksheet.write(row, col, coeffs[col][row]) # horizontal
                
                
                            # Insert an image - useful for documentation export ?!.
                #            worksheet.insert_image('B5', 'logo.png')
                
                            workbook.close()
                
                        else:
                            logger.error('Unknown file type "%s"', file_type)
                            file_type_err = True
                            
                        if not file_type_err:
                            logger.info('Filter saved as "%s"', file_name)
                            rc.save_dir = os.path.dirname(file_name) # save new dir
                    
            except IOError as e:
                logger.error('Failed saving "%s"!\n%s\n', file_name, e)

    
            # Download the Simple ods py module:
            # http://simple-odspy.sourceforge.net/
            # http://codextechnicanum.blogspot.de/2014/02/write-ods-for-libreoffice-calc-from_1.html

#------------------------------------------------------------------------------
    def import_coeffs(self):
        """
        Import filter coefficients from a file
        """
        file_filters = ("Matlab-Workspace (*.mat);;Binary Numpy Array (*.npy);;"
        "Zipped Binary Numpy Array(*.npz)")
        dlg = QFD(self)
        file_name, file_type = dlg.getOpenFileName_(
                caption = "Import filter coefficients ", 
                directory = rc.save_dir, filter = file_filters)
        file_name = str(file_name) # QString -> str

        for t in extract_file_ext(file_filters): # extract the list of file extensions
            if t in str(file_type):
                file_type = t
        
        if file_name != '': # cancelled file operation returns empty string 
        
            # strip extension from returned file name (if any) + append file type:
            file_name = os.path.splitext(file_name)[0] + file_type   

            file_type_err = False
            try:
                with io.open(file_name, 'rb') as f:
                    if file_type == '.mat':
                        data = scipy.io.loadmat(f)
                        fb.fil[0]['ba'] = data['ba']
                    elif file_type == '.npy':
                        fb.fil[0]['ba'] = np.load(f)
                        # can only store one array in the file
                    elif file_type == '.npz':
                        fb.fil[0]['ba'] = np.load(f)['ba']
                        # would be possible to store several arrays in one file
                    else:
                        logger.error('Unknown file type "%s"', file_type)
                        file_type_err = True
                        
                    if not file_type_err:
                        logger.info('Loaded coefficient file\n"%s"', file_name)
                        self.sigFilterLoaded.emit()
                        rc.save_dir = os.path.dirname(file_name)
            except IOError as e:
                logger.error("Failed loading %s!\n%s", file_name, e)
        

#------------------------------------------------------------------------------
    def save_file_coe(self, file_name):
        """
        Save filter coefficients in Xilinx coefficient format, specifying
        the number base and the quantized coefficients
        """

        frmt = fb.fil[0]['q_coeff']['frmt'] # store old format
        fb.fil[0]['q_coeff']['frmt'] = 'int' # 'hex'
        qc = fix_lib.Fixed(fb.fil[0]['q_coeff'])
        bq = qc.fix(fb.fil[0]['ba'][0]) # Quantize coefficients to integer format
        coe_width = qc.WF + qc.WI + 1 # quantized word length; Int. + Frac. + Sign bit
        if fb.fil[0]['q_coeff']['frmt'] == 'int':
            coe_radix = 10
        else:
            coe_radix = 16

        fb.fil[0]['q_coeff']['frmt'] = frmt # restore old coefficient format

        info_str = (
            "; #############################################################################\n"
             ";\n; XILINX CORE Generator(tm) Distributed Arithmetic FIR filter coefficient (.COE) file\n"
             ";\n; Generated by pyFDA 0.1 (https://github.com/chipmuenk/pyfda)\n;\n; ")
        date_str = datetime.datetime.now().strftime("%d-%B-%Y %H:%M:%S")

        file_name.write(info_str + date_str + "\n;\n")
        filt_str = "; Filter order = %d, type: %s\n" %(fb.fil[0]["N"], fb.fil[0]['rt'])
        file_name.write(filt_str)
        file_name.write("; #############################################################################\n")
        file_name.write("Radix = %d;\n" %coe_radix)
        file_name.write("Coefficient_width = %d;\n" %coe_width)
        coeff_str = "CoefData = "
        for b in bq:
            coeff_str += str(b) + ",\n"
        file_name.write(coeff_str[:-2] + ";") # replace last "," by ";"


#------------------------------------------------------------------------------

if __name__ == '__main__':

    from ..compat import QApplication
    app = QApplication(sys.argv)
    mainw = File_IO(None)

    app.setActiveWindow(mainw) 
    mainw.show()

    sys.exit(app.exec_())