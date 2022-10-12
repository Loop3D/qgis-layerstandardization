# -*- coding: utf-8 -*-
"""
/***************************************************************************
 LayerStandardizationDialog
                                 A QGIS plugin
 This plugin standardize the layer columns and row id before it is used for map2loop
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2022-09-13
        git sha              : $Format:%H$
        copyright            : (C) 2022 by Michel Nzikou
        email                : michel.nzikou@alumni.uleth.ca
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
#########
# Import the code for the DockWidget
import os
import sys
from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QComboBox,QLabel,QAction, QFileDialog, QMessageBox, QTreeWidgetItem,QTextEdit,QVBoxLayout
from qgis.utils import iface
from qgis.core import QgsSettings
from PyQt5.QtCore import QRect
from PyQt5.QtGui import QFont
#####
import os.path
from .Load_Vectors import shapeFileloader,xLayerReader,create_json_file
from .CreatePythonFile import create_a_python_file
#
# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'layer_standardization_dialog_base.ui'))

##################################################################
class LayerStandardizationDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(LayerStandardizationDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        ###############################
        self.setupUi(self)
        #self.selectedFolder=None
        ### Toggle check box
        self.SearchFolder.setEnabled(False)
        ######
        self.Folder_checkBox.pressed.connect(self.select_folder)
        ################ add Geology and save its layer param into a list
        self.GeolButton.clicked.connect(self.create_geology_IdName)
        self.GeolButton.clicked.connect(self.GeolLayerbtnstate)
        self.Save_pushButton.clicked.connect(self.save_geol_IdName)
        #################   add Fault and save its layer param into a list 
        self.FaultButton.clicked.connect(self.create_fault_IdName)
        self.FaultButton.clicked.connect(self.FaultLayerbtnstate)
        self.Save_pushButton.clicked.connect(self.save_fault_IdName)
        ################# add struct and save its layer param into a list
        self.StructButton.clicked.connect(self.create_struct_IdName)
        self.StructButton.clicked.connect(self.StructLayerbtnstate)
        self.Save_pushButton.clicked.connect(self.save_struct_IdName)
        ################# Below we are pushing default data for Fold and Mineral Deposit Layer
        self.MinDepositButton.clicked.connect(self.save_MineralDeposit_IdName)
        self.FoldButton.clicked.connect(self.save_Fold_IdName)
        ################# Create json file
        self.Json_pushButton.clicked.connect(self.createJson)    
        ################# Create py file
        self.CreatePyButton.clicked.connect(self.save_your_python_file) 
#**********************************************************************************************************
 ############################################################################################################       
    # ##### This function  select folder name/project name from it's folder
    def select_folder(self):
        foldername = QFileDialog.getExistingDirectory(self.Folder_checkBox, "Select folder ","",)
        self.SearchFolder.setText(foldername)
        self.Folder_checkBox.setChecked(True)
        return 
    ###### This function activate Layer into a qgis workspace and return the layer_name list (Col name of the table)
    def activate_layers(self):
        title = self.GeolButton.text()
        shape_file_list = []
        for shape_file in QFileDialog.getOpenFileNames(self, title):
            shape_file_list.append(shape_file)
        list_of_files     = shape_file_list[0]
        self.path_file    = list_of_files[0]
        colNames          = shapeFileloader(list_of_files)
        return colNames,self.path_file
#**********************************************************************************************************
############################################################################################################
    ### This function create Geology ID Name and for all combobox available
    ### X,Y .. defined the new position of the QLineEdit and Qlabel position when the Fault Layer is selected
    def create_geology_IdName(self): 
            p,self.GeolPath=self.activate_layers()   ## This help select the shapefile
            if self.GeolButton.objectName()=='GeolButton':
                self.GeolPath=self.GeolPath
            geol_comboHeader = ['Formation*', 'Group*','Supergroup*', 'Description*', 'Fm code*', 'Rocktype 1*','Rocktype 2*','Polygon ID*','Min Age*','Max Age*']
            colNames         = xLayerReader()
            #for col in colNames:
            self.combo_column_appender(colNames)        # This code add element in combo items
            self.label_replacer(geol_comboHeader)      # This code changes 1st item of combo box
            Sill_Msg=" Enter Sill Text:"
            Intr_Msg=" Enter Intrusion Text:"
            X1=630
            Y1=170
            X2=632
            Y2=190
            X3=630
            Y3=250
            X4=632
            Y4=270
            ## The below section transform the label and QLineEditor and move it to X and Y
            self.dynamic_label(Sill_Msg,self.Sill_Label,X1,Y1)
            self.dynamic_QEditor(self.Sill_LineEditor,X2,Y2)
            self.dynamic_label(Intr_Msg,self.Intrusion_Label,X3,Y3)
            self.dynamic_QEditor(self.Intrusion_LineEditor,X4,Y4)
            return
############################################################################################################
    ### This function create fault ID Name and for the combobox 4=Dip Direction type* only ['num','alpha'] available
    ### X,Y .. defined the new position of the QLineEdit and Qlabel position when the Fault Layer is selected
    def create_fault_IdName(self):
            p,self.FaultPath=self.activate_layers()                                    # This help select the shapefile
            if self.FaultButton.objectName()=='FaultButton':
                self.FaultPath=self.FaultPath
            fault_comboHeader = ['Default Dip*', 'Dip Direction*','Feature*', 'Dip Direction type*', 'fdipest*', 'Point ID*',' ',' ',' ',' ']
            colNames          = xLayerReader()
            self.combo_column_appender(colNames)                                        # This code add element in combo items
                ### Transform
            DipDirectionConv_colNames =[' ','num','alpha']                             # Empty label is set for the Header name
            self.cmbDescriptionLayerIDName.clear()                                     # Clear the Dip Direction Convention* box
            self.cmbDescriptionLayerIDName.addItems(DipDirectionConv_colNames)         # Clear the Dip Direction Convention* box
            self.label_replacer(fault_comboHeader)                                     # This code changes 1st item of combo box
            Fault_Msg =" Enter Fault Text:"
            Fdipes_Msg=" Enter fdipest Text:"
            X1=608
            Y1=130
            X2=610
            Y2=150
            X3=608
            Y3=210
            X4=610
            Y4=230
            ## The below section transform the label and QLineEditor and move it to X and Y
            self.dynamic_label(Fault_Msg,self.Sill_Label,X1,Y1)
            self.dynamic_QEditor(self.Sill_LineEditor,X2,Y2)
            self.dynamic_label(Fdipes_Msg,self.Intrusion_Label,X3,Y3)
            self.dynamic_QEditor(self.Intrusion_LineEditor,X4,Y4)
            return
############################################################################################################
    ### This function create Structure Layer ID Name and for the combobox 4=Dip Direction convention* only ['Strike','Dip Direction'] available
    ### X,Y .. defined the new position of the QLineEdit and Qlabel position when the Fault Layer is selected
    def create_struct_IdName(self):
            p,self.StructPath=self.activate_layers()                                   # This help select the shapefile
            if self.StructButton.objectName()=='StructButton':
                self.StructPath=self.StructPath 
            fault_comboHeader  = ['Dip*', 'Dip Direction*','Feature*', 'Dip Direction Convention*', 'Overturned Field*', 'Point ID*',' ',' ',' ',' ']
            colNames           = xLayerReader()
            self.combo_column_appender(colNames)
            ### Transform
            DipDirectionConv_colNames =[' ','Strike','Dip Direction']                  # Empty label is set for the Header name
            self.cmbDescriptionLayerIDName.clear()                                     # Clear the Dip Direction Convention* box
            self.cmbDescriptionLayerIDName.addItems(DipDirectionConv_colNames)         # Clear the Dip Direction Convention* box
            self.label_replacer(fault_comboHeader)                                     # This code changes 1st item of combo box
            bedding_Msg =" Enter bedding Text:"
            Overtune_Msg=" Enter Overturned Text:"
            X1=608
            Y1=130
            X2=610
            Y2=150
            X3=608
            Y3=210
            X4=610
            Y4=230
            ## The below section transform the label and QLineEditor and move it to X and Y
            self.dynamic_label(bedding_Msg,self.Sill_Label,X1,Y1)
            self.dynamic_QEditor(self.Sill_LineEditor,X2,Y2)
            self.dynamic_label(Overtune_Msg,self.Intrusion_Label,X3,Y3)
            self.dynamic_QEditor(self.Intrusion_LineEditor,X4,Y4)
            return
#**********************************************************************************************************
############################################################################################################
    ###### This function save selected geology Layer ID name from the scrolldown and also entered value from the Qlineeditor
    def save_geol_IdName(self):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                    self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                    self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                    self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                    self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        combo_flag    = self.cmbFormationLayerIDName.itemText(0)
        if combo_flag == 'Formation*':
            geol_data = []           
            for i in range(10):
                geol_data.append(self.my_combo_list[i].currentText())
                self.my_combo_list[i].clear()
            self.Sill_input      = self.Sill_LineEditor.text()
            self.Intrusion_input = self.Intrusion_LineEditor.text()
            self.a_sill          = self.default_input(self.Sill_input,'sill')
            self.a_intrusion     = self.default_input(self.Intrusion_input,'intrusive')
            self.geol_data       = geol_data+[str(self.a_sill),str(self.a_intrusion)]
            self.btnstate(self.GeolButton,'Geology params were saved')
            self.Sill_LineEditor.clear()                                                 ## This line clear the QLineEditor text box
            self.Intrusion_LineEditor.clear()                                            ## This line clear the QLineEditor text box
        return 
############################################################################################################
###### This function save fault Layer ID name into a scroll down search
    def save_fault_IdName(self):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                    self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                    self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                    self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                    self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        combo_flag     = self.cmbFormationLayerIDName.itemText(0)
        if combo_flag  == 'Default Dip*':
            fault_data =[]
            for i in range(10):
                fault_data.append(self.my_combo_list[i].currentText())
                self.my_combo_list[i].clear()
            self.fault_input     = self.Sill_LineEditor.text()
            self.fdipest_input   = self.Intrusion_LineEditor.text()
            self.a_fault         = self.default_input(self.fault_input,'Fault')
            self.a_fdipest       = self.default_input(self.fdipest_input,'shallow,steep,vertical')
            self.fault_data      = fault_data[0:6]+[str(self.a_fault),str(self.a_fdipest)]  #
            self.btnstate(self.FaultButton,'Fault params were saved')
            self.Sill_LineEditor.clear()
            self.Intrusion_LineEditor.clear()
        return
############################################################################################################
###### This function save Structure/Point Layer ID name into a scroll down search
    def save_struct_IdName(self):
        self.clear_combo_list()
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                    self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                    self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                    self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                    self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        combo_flag      = self.cmbFormationLayerIDName.itemText(0)
        if combo_flag   == 'Dip*':
            struct_data =[]
            for i in range(10):
                struct_data.append(self.my_combo_list[i].currentText())
                self.my_combo_list[i].clear()
            self.bedding_input     = self.Sill_LineEditor.text()
            self.overtune_input    = self.Intrusion_LineEditor.text()
            self.a_bedding         = self.default_input(self.bedding_input ,'Bed')
            self.a_overtune        = self.default_input(self.overtune_input,'overturned')
            self.struct_data       = struct_data[0:6]+[str(self.a_bedding),str(self.a_overtune)]  #
            self.btnstate(self.StructButton,'Structure params were saved')
            self.Sill_LineEditor.clear()
            self.Intrusion_LineEditor.clear()
        return
############################################################################################################
    def save_MineralDeposit_IdName(self):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
            self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
            self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
            self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
            self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        self.mindeposit_data = ['site_code', 'short_name', 'site_type_','target_com','site_commo','commodity_','infrastructure']
        for i in range(10):
            self.my_combo_list[i].clear()
        self.btnstate(self.MinDepositButton,'Min Deposit params were saved')
############################################################################################################
    def save_Fold_IdName(self):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
            self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
            self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
            self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
            self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        self.fold_data      = ['feature', 'Fold axial trace', 'type','syncline']
        for i in range(10):
            self.my_combo_list[i].clear()
        self.btnstate(self.FoldButton,'Fold params were saved')
#**********************************************************************************************************
############################################################################################################
    def createJson(self):
        try:
            self.default_data     = [ 'volc', '0','No_col','500']  # Hard Coded default data
            self.Alldata          = self.geol_data+self.fault_data+self.struct_data+self.mindeposit_data+self.fold_data+self.default_data
            geol_listKeys         = ['c','g','g2','ds','u','r1','r2','o-geol','min','max','sill','intrusive'] #o-geol is initially o
            fault_listKeys        = ['fdip','fdipdir','f','fdipdir_flag','fdipest','o','fault','fdipest_vals']    
            struct_listKeys       = ['d','dd','sf','otype','bo','gi','bedding','btype'] #o-struct is initially o 
            mindeposit_lisKeys    = ['msc','msn','mst','mtc','mscm','mcom','minf']
            fold_lisKeys          = ['ff','fold','t','syn']
            default_keys          = ['volcanic','fdipnull','n','deposit_dist']  # Hard Coded default data keys
            AllKeys               = geol_listKeys + fault_listKeys + struct_listKeys + mindeposit_lisKeys + fold_lisKeys + default_keys
            formation_data        = dict(zip(AllKeys, self.Alldata))
            json_path             = self.SearchFolder.text()
            try:
               #print('formation data {}'.format(formation_data))
               create_json_file(json_path,formation_data)
               QMessageBox.about(self,"STATUS", "*****json file created*****")
            except:
                buttonReply = QMessageBox.question(self, 'OOPS Path Not Selected', "Do you want to continue?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        except:
            buttonReply = QMessageBox.question(self, 'OOPS Load all Layers', "Do you want to continue?", QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        return
############################################################################################################
## This function send a message to the console such as: the data were saved
## This function create the save label msg once the layer QPushbutton is activated & the save button pushed
    def btnstate(self, label1, Msg):
            self.Msg =Msg
            if label1.isEnabled():
                label=self.Console_Label
                label.setText('Console: '+str(self.Msg))
                label.setFont(QFont("Sanserif",14))
            else:
                self.Msg = "No params were saved"
                print(str(self.Msg))
                label=self.Console_Label
                label.setText('Console: '+str(self.Msg))
                label.setFont(QFont("Sanserif",14))
            return
############################################################################################################
    def GeolLayerbtnstate(self):
        if not self.GeolButton.isChecked():
            Msg = "Geology Layer is loaded"
            label=self.Console_Label
            label.setText('Console: '+str(Msg))
            label.setFont(QFont("Sanserif",14))
        return
    def FaultLayerbtnstate(self):
        if not self.FaultButton.isChecked():
            Msg="Fault Layer is loaded"
            label=self.Console_Label
            label.setText('Console: '+str(Msg))
            label.setFont(QFont("Sanserif",14))
        return
    def StructLayerbtnstate(self):
        if not self.StructButton.isChecked():
            Msg="Structure Layer is loaded"
            label=self.Console_Label
            label.setText('Console: '+str(Msg))
            label.setFont(QFont("Sanserif",14))
        return
############################################################################################################
     ###### This function change combo title based on the layer name
    def label_replacer(self,list_of_element):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                            self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                            self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                            self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                            self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        for id,replace_elt in enumerate(self.my_combo_list):
            replace_elt.setItemText(0, list_of_element[id])
        return
############################################################################################################
     ###### This function append combo elt to all layer name
    def combo_column_appender(self,col_list):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                            self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                            self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                            self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                            self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        for id,elt2 in enumerate(self.my_combo_list):
            if not self.cmbFormationLayerIDName:
                elt2.addItems(['']+col_list)
            else:
                elt2.addItems(col_list)  
        return
############################################################################################################
    def default_input(self, value,input_tag):
        # This function return either empty QLineEdit string or the value typed in.
        value     =value
        input_tag =input_tag
        if not value:
            self.val =str(input_tag)
        else:
            self.val =value
        return self.val
############################################################################################################
    ## This function create dynamic label which is then move into X1,Y1 position
    def dynamic_label(self, Sill_Msg,label1,X1,Y1): #Sill_Msg is the message title on top op your QLineEditor
        label =label1                               #label1 is the name of the qt designer feature i.e self.Combobox, 
        label.setText(Sill_Msg)                     # X1,Y1 is the (x,y) coordinate of the feature into the MainWindow
        label.setFont(QFont("Sanserif",10))
        label1.move(X1,Y1)
############################################################################################################
    ## This function create dynamic QEditor which is then move into X1,Y1 position
    def dynamic_QEditor(self,label1,X1,Y1):
        label =label1
        label1.move(X1,Y1)
############################################################################################################
###### This function save Structure/Point Layer ID name into a scroll down search
    def clear_combo_list(self):
        self.my_combo_list =[self.cmbFormationLayerIDName,self.cmbGroupLayerIDName,
                    self.cmbSupergroupLayerIDName,self.cmbDescriptionLayerIDName,
                    self.cmbFmLayerIDName, self.cmbRocktype1LayerIDName,
                    self.cmbRocktype2LayerIDName,self.cmbPointIDLayerIDName,
                    self.cmbMinAgeLayerIDName,self.cmbMaxAgeLayerIDName]
        for i in range(10):
            self.my_combo_list[i].clear    
        return 
############################################################################################################
    def save_your_python_file(self):
        self.filepath     = self.SearchFolder.text()
        self.pyfilename   = 'Run_test'                     ##  This is the name of the python file created
        geology_filename  = str(self.GeolPath)
        fault_filename    = str(self.FaultPath)
        fold_filename     = str(self.FaultPath)
        structure_filename= str(self.StructPath)
        dtm_filename      = 'http://services.ga.gov.au/gis/services/DEM_SRTM_1Second_over_Bathymetry_Topography/MapServer/WCSServer?'
        metadata_filename = str(self.filepath)+'/'+'data.json'
        mindep_filename   = 'http://13.211.217.129:8080/geoserver/loop/wms?service=WMS&version=1.1.0&request=GetMap&layers=loop%3Anull_mindeps'
        overwrite         = 'true'
        verbose_level     = 'VerboseLevel.NONE'
        project_path      = str(self.filepath)
        working_projection= 'epsg:28350'
        # ### Here we define data2 paramas
        out_dir           =str(self.filepath)
        bbox_3d           ={'minx': 520000, 'miny': 7490000, 'maxx': 550000, 'maxy': 7510000, 'base': -3200, 'top': 1200}
        run_flags         ={'aus': True, 'close_dip': -999.0, 'contact_decimate': 5, 'contact_dip': -999.0, 'contact_orientation_decimate': 5, 'deposits': 'Fe,Cu,Au,NONE', 'dist_buffer': 10.0, 'dtb': '', 'fat_step': 750.0, 'fault_decimate': 5, 'fault_dip': 90.0, 'fold_decimate': 5, 'interpolation_scheme': 'scipy_rbf', 'interpolation_spacing': 500.0, 'intrusion_mode': 0, 'max_thickness_allowed': 10000.0, 'min_fault_length': 5000.0, 'misorientation': 30.0, 'null_scheme': 'null_scheme', 'orientation_decimate': 0, 'pluton_dip': 45.0, 'pluton_form': 'domes', 'thickness_buffer': 5000.0, 'use_fat': False, 'use_interpolations': False, 'fault_orientation_clusters': 2, 'fault_length_clusters': 2, 'use_roi_clip': False, 'roi_clip_path': ''}
        proj_crs          ='epsg:28350'
        clut_path         =''
        ### data4 is used to copy a specific file <map2loop.qgz> into a project path <proj.config.project_path+/>
        qgz_file          ='./source_data/map2loop.qgz'
        qgz_split_name    = qgz_file.split('/')[-1]
        #### Module_Import is the import module variable
        Module_Import     = 'from map2loop.project import Project \nfrom map2loop.m2l_enums import VerboseLevel \nimport shutil\n'
        #### project_config create a project with defined specific params
        project_config    = 'proj = Project(\n''                geology_filename='+"'"+str(geology_filename)+"'"+',''\n                fault_filename='+"'"+str(fault_filename)+"'"+',\n                fold_filename='+"'"+str(fold_filename)+"'"+',\n                structure_filename='+"'"+str(structure_filename)+"'"+',\n                mindep_filename='+"'"+str(mindep_filename)+"'"+',\n                dtm_filename='+"'"+str(dtm_filename)+"'"+',\n                metadata_filename='+"'"+str(metadata_filename)+"'"+',\n                overwrite='"'"+str(overwrite)+"'"+',\n                verbose_level=VerboseLevel.NONE'+',\n                project_path='+"'"+str(project_path)+"'"+',\n                working_projection='+"'"+str(working_projection)+"'"+',\n                )'
        #### project_update update the configuration files 
        project_update    = '\n \nproj.update_config(\n                    out_dir='+"'"+str(out_dir)+"'"+',\n                    bbox_3d='+str(bbox_3d)+',\n                    run_flags='+str(run_flags)+',\n                    proj_crs='+"'"+ str(proj_crs)+"'"+',\n                    clut_path='+"'"+str(clut_path)+"'"+',\n                )'
        #### project_run is used to run the proj
        project_run       = '\n \nproj.run()\n' 
        #### copy file qgz file into a different location
        proj_dest         = 'proj.config.project_path'
        qgz_move          = '/'+ str(qgz_split_name)
        copyqgzfile       = 'shutil.copyfile('+"'"+ str(qgz_file)+"'"+ ', '+str(proj_dest)+"+'"+ str(qgz_move)+"'"+ ')'
        #######################
        create_a_python_file(self.filepath,self.pyfilename,Module_Import,project_config,project_update,project_run,copyqgzfile)
        QMessageBox.about(self,"STATUS", "*****python file created*****")
###############################################################################################################################################################################