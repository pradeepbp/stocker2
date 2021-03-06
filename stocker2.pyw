#!/usr/bin/python


'''
stocker2.pyw
Copyright (C) 2011 Pradeep Balan Pillai

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

'''
This is the initialiser which creats the basic GUI and offers the user
the choice of program components like watchlist, stocklist, portfolio etc.
'''

import gtk

import watchlist
import stocklist
import dialogs


class MainGUI:
    def __init__(self):
        self.content_flag = '' # Indicates the content of main view to other GUI compo.
        self.draw_Main_Window()
        self.dialogfactory = dialogs.DialogFactory()
        self.stocklist = stocklist.StockList()


    '''
    Adds stock to a list.
    Function will check for the current selected option and accordingly initiate the
    correct dialog box
    '''
    # Callback function to Add stock to stocklist
    def add_stock(self):
        self.result_buffer.set_text('adding stock to stocklist')
        stock = self.dialogfactory.get_info_dialog(['Display Name', 'Stock Code'])
        if stock != False:
            self.stocklist.append_stock(stock)

    # Callback function to Delete stock from stocklist
    def del_stock(self):
        selected_items = self.dialogfactory.item_choose_dialog('Delete stock',None,
                            'Select stocks to delete',None,None,
                            (self.stocklist.get_stocklist()).keys())
        if selected_items != False:
            deleted = self.stocklist.delete_stocks(selected_items)
            if deleted == False:
                warn = gtk.MessageDialog(None,gtk.DIALOG_MODAL,gtk.MESSAGE_WARNING,
                                    gtk.BUTTONS_OK,'Nothing to delete')
                resp = warn.run()
                if resp == gtk.RESPONSE_OK:
                    warn.destroy()
                                    
    '''
    Callback function to add stocks to watchlist. The user is prompted to choose from the 
    stocklist
    '''
    def add_stocks_to_watchlist(self):
        selected_items = self.dialogfactory.item_choose_dialog('Add stocks', None,
                            'Select stocks to add to watchlist', None, None,
                             (self.stocklist.get_stocklist()).keys())



    #Function to create main window ans initialise the GUI components
    def draw_Main_Window(self):
        self.main_window = gtk.Window()
        self.main_window.set_default_size(gtk.gdk.screen_width(),
                                            gtk.gdk.screen_height())
        self.main_window.set_position(gtk.WIN_POS_CENTER)
        self.main_window.connect('destroy', gtk.main_quit)
        table = gtk.Table(4,1, False)

        #Create menu bar and menu items
        menu_bar = gtk.MenuBar()

        #File menu
        file_menu = gtk.MenuItem('_File', True)
        file_submenu = gtk.Menu()
        file_menu.set_submenu(file_submenu)
        menu_bar.append(file_menu)

        file_menu_item_exit = gtk.MenuItem('E_xit', True)
        file_menu_item_exit.connect('activate', gtk.main_quit)
        file_submenu.append(file_menu_item_exit)

        # Edit Menu
        edit_menu = gtk.MenuItem('_Edit', True)
        edit_submenu = gtk.Menu()
        edit_menu.set_submenu(edit_submenu)
        menu_bar.append(edit_menu)

        edit_stocklist = gtk.MenuItem('_Stocklist', True)
        edit_stocklist_submenu = gtk.Menu()
        edit_stocklist.set_submenu(edit_stocklist_submenu)

        edit_submenu.append(edit_stocklist)
        edit_stocklist_addstock = gtk.MenuItem('_Add stock...', True)
        edit_stocklist_submenu.append(edit_stocklist_addstock)
        edit_stocklist_addstock.connect('activate', (lambda a: self.add_stock()))
        
        edit_stocklist_delstock = gtk.MenuItem('_Delete stock...', True)
        edit_stocklist_submenu.append(edit_stocklist_delstock)
        edit_stocklist_delstock.connect('activate', lambda a: self.del_stock())
       
        edit_watchlist = gtk.MenuItem('_Watchlist', True)
        edit_watchlist_submenu = gtk.Menu()
        edit_watchlist.set_submenu(edit_watchlist_submenu)
        edit_watchlist_addstock = gtk.MenuItem('_Add stock...', True)
        edit_watchlist_delstock = gtk.MenuItem('_Delete stock...', True)
        edit_watchlist_submenu.append(edit_watchlist_addstock)
        edit_watchlist_submenu.append(edit_watchlist_delstock)
        edit_submenu.append(edit_watchlist)
        edit_watchlist_addstock.connect('activate', lambda a: self.add_stocks_to_watchlist())


        # View menu
        view_menu= gtk.MenuItem('_View', True)
        view_submenu = gtk.Menu()
        view_menu.set_submenu(view_submenu)
        menu_bar.append(view_menu)


        view_menu_item_mystocklist = gtk.MenuItem('_My Stock List', True)
        view_submenu.append(view_menu_item_mystocklist)
        view_menu_item_mystocklist.connect('activate', lambda w: self.show_mystocklist())

        view_menu_item_watchlist = gtk.MenuItem('_Watchlist', True)
        view_menu_item_watchlist.connect('activate',
                                        (lambda stocker: self.show_watchlist()))
        view_submenu.append(view_menu_item_watchlist)

        #Create status bar to flash messages
        self.status_bar = gtk.Statusbar()
        self.status_bar.push(self.status_bar.get_context_id('Initial message'),'Open')

        # Create an area where results of user commands in plain text can be displayed
        # Graphical results shall be drawn to a separate widget
        scroll = gtk.ScrolledWindow()
        scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.result_buffer = gtk.TextBuffer(None)
        self.result_buffer.set_text('Result pane')
        result_area = gtk.TextView(self.result_buffer)
        result_area.set_editable(False)
        scroll.add_with_viewport(result_area)


        # Add GUI components to the layout
        table.attach(menu_bar, 0,1,0,1, gtk.EXPAND|gtk.FILL, gtk.SHRINK)
        table.attach(scroll, 0,1,2,3, yoptions = gtk.EXPAND|gtk.FILL)
        table.attach(self.status_bar, 0,1,3,4, xoptions=gtk.EXPAND|gtk.FILL,
                    yoptions=gtk.SHRINK)

        self.main_window.add(table)
        self.main_window.show_all()

    # This funciton will display the watchlist
    def show_watchlist(self):
        self.content_flag = 'wl' 
        self.watchlist = watchlist.Watchlist()
        self.status_bar.push(1, 'Loading tickers...') # load tickers from pickled file
        self.watchlist.load_tickers()
        string = ''
        for item in self.watchlist.tickers.keys():
            string = string + self.watchlist.tickers[item] + '\n'
        self.result_buffer.set_text(string)

    # View the detailed list of preferred stocks in a dialog box
    def show_mystocklist(self):
        self.content_flag = 'sl'
        self.status_bar.push(1, 'My Stocklist')
        list_to_display = self.stocklist.get_stocklist()
        list_in_plain_text = ''
        for key in list_to_display.keys():
            list_in_plain_text = (list_in_plain_text + key 
                                    + ':' + list_to_display[key] + '\n') 
        self.result_buffer.set_text('----- Stock List ------\n'+list_in_plain_text)
        
if __name__=='__main__':
    MainGUI()
    gtk.main()
