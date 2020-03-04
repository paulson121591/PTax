import sys

import taxjar
from PySide2.QtCore import QFile, QObject
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QLineEdit, QComboBox, QPushButton, QApplication
from uszipcode import SearchEngine

client = taxjar.Client( api_key='b945f7cd7180bf57e187f91e84cf76e0' )


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

        self.pushButtonLook.clicked.connect( self.look )
        self.lineEditZip.editingFinished.connect( self.zipcity )
        self.lineEditAddress.editingFinished.connect( self.zipcity )

        self.window.show()

    def look(self):


        # noinspection PyPep8Naming
        zipCode = self.lineEditZip.text()
        city = self.lineEditCity.currentText()
        street = self.lineEditAddress.text()

        rates = client.rates_for_location( zipCode, {'city': city, 'street': street} )
        county = rates.county
        self.lineEditCounty.setText( str( county ) )

        tax = rates['combined_rate']

        tax = tax * 100

        tax = round( tax, 2 )
        search = SearchEngine( simple_zipcode=True )
        zipcode = search.by_zipcode( zipCode )
        self.lineEditRate.setText( str( tax ) + '%' )

    def zipcity(self):
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



if __name__ == '__main__':
    app = QApplication( sys.argv )
    form = Form( 'mainwindow.ui' )
    sys.exit( app.exec_() )
