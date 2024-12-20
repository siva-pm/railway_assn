import streamlit as st

from streamlit_option_menu import option_menu

import home,accounts,stats,more

st.set_page_config(
    page_title='money manager')

class multiapp:
    def __init__(self):
        self.apps=[]
    
    def add_app (self,title,function):
        self.apps.append(
            {"title":title,
             "function":function
            }
        )
    
    def run(self):
        with st.sidebar:
            app=option_menu(
                menu_title='MAIN MENU',
                options=['home','stats','accounts','more']
            )
        if app=='home':
            home.app()
        if app=='accounts':
            accounts.app()
        if app=='stats':
            stats.app()
        if app=='more':
            more.app()
appa=multiapp()
appa.run() 
