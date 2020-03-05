import sys
import time

import taxjar
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from uszipcode import SearchEngine
import sqlalchemy.sql.default_comparator
import pyautogui
import pickle
license_fetch = pickle.load(open('license','rb'))
license_key = license_fetch.get('New license','')



class Form( QObject ):

    def __init__(self, ui_file, parent=None):
        super( Form, self ).__init__( parent )
        ui_file = QFile( ui_file )
        ui_file.open( QFile.ReadOnly )

        loader = QUiLoader()
        self.window = loader.load( ui_file )
        ui_file.close()




        self.lineEditZip = self.window.findChild( QLineEdit, 'lineEditZip' )
        self.lineEditCity = self.window.findChild( QComboBox, 'lineEditCity' )
        self.lineEditCounty = self.window.findChild( QLineEdit, 'lineEditCounty' )
        self.lineEditAddress = self.window.findChild( QLineEdit, 'lineEditAddress' )
        self.lineEditRate = self.window.findChild( QLineEdit, 'lineEditRate' )
        self.pushButtonLook = self.window.findChild( QPushButton, 'pushButtonLook' )
        self.actionLicense = self.window.findChild( QAction, 'actionLicense' )
        self.lineEditBeTax = self.window.findChild( QLineEdit, 'lineEditBeTax' )
        self.lineEditAfTax = self.window.findChild( QLineEdit, 'lineEditAfTax' )

        self.pushButtonLook.clicked.connect( self.look )
        self.lineEditZip.editingFinished.connect( self.zipcity )
        self.lineEditAddress.editingFinished.connect( self.zipcity )
        self.actionLicense.triggered.connect(self.license)
        if self.lineEditRate.text != '':
            self.lineEditBeTax.editingFinished.connect(self.look)

        self.window.show()

    def look(self,):
        try:
            client = taxjar.Client( api_key=license_key )



            # noinspection PyPep8Naming
            self.lineEditRate.clear()
            zipCode = self.lineEditZip.text()
            city = self.lineEditCity.currentText()
            street = self.lineEditAddress.text()

            rates = client.rates_for_location( zipCode, {'city': city, 'street': street} )
            county = rates.county
            self.lineEditCounty.setText( str( county ) )

            tax = rates['combined_rate']

            try:
                lineEditBeTax = self.lineEditBeTax.text()

                total_price = (tax * float(lineEditBeTax))+float(lineEditBeTax)
                self.lineEditAfTax.setText('$'+str(total_price))
            except:
                print('no price')



            tax = tax * 100

            tax = round( tax, 2 )
            search = SearchEngine( simple_zipcode=True )
            zipcode = search.by_zipcode( zipCode )
            self.lineEditRate.setText( str( tax ) + '%' )


        except taxjar.exceptions.TaxJarResponseError as err:
            if '401' in str(err):
                pyautogui.alert('Check license_key\n  '+ str(err))
            if '404' in str(err):
                pyautogui.alert( 'not found check the info and try again\n ' + str( err ) )





    def zipcity(self,):
        client = taxjar.Client( api_key=license_key )
        street = self.lineEditAddress.text()

        # noinspection PyPep8Naming
        zipCode = self.lineEditZip.text()
        city = self.lineEditCity.currentText()
        search = SearchEngine( simple_zipcode=True )
        zipcode = search.by_zipcode( zipCode )

        zipcodecity = zipcode.common_city_list
        rates = client.rates_for_location( zipCode, {'city': zipcodecity, 'street': street} )
        county = rates.county
        self.lineEditCounty.setText( str( county ) )

        self.lineEditCounty.clear()

        self.lineEditCity.clear()

        self.lineEditCounty.setText( str( county ) )

        self.lineEditCity.addItems( zipcodecity )

    def license(self):
        updatelicense = pyautogui.prompt('enter new license code')
        newlicense ={'New license':updatelicense}

        if updatelicense != None:
            pickle.dump( newlicense, open( 'license', "wb") )












if __name__ == '__main__':



    app = QApplication( sys.argv )

    splash_pix = QPixmap( 'Splash.png' )

    splash = QSplashScreen( splash_pix, Qt.WindowStaysOnTopHint )
    splash.setWindowFlags( Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint )
    splash.setEnabled( False )
    # splash = QSplashScreen(splash_pix)
    # adding progress bar
    progressBar = QProgressBar( splash )
    progressBar.setMaximum( 10 )
    progressBar.setGeometry( 0, splash_pix.height() - 60, splash_pix.width(), 20 )

    # splash.setMask(splash_pix.mask())

    splash.show()
    splash.showMessage( "<h1><font color='white'>Getting things set up</font></h1>", Qt.AlignBottom | Qt.AlignCenter, Qt.black )

    for i in range( 1, 11 ):
        progressBar.setValue( i )
        t = time.time()
        while time.time() < t + 0.1:
            app.processEvents()
    splash.showMessage( "<h1><font color='white'>Checking License Almost Ready! </font></h1>", Qt.AlignBottom | Qt.AlignCenter,
                        Qt.black )

    # Simulate something that takes time
    time.sleep( 2 )

    form = Form( 'mainwindow.ui' )

    splash.finish(form.window)
    sys.exit( app.exec_() )
