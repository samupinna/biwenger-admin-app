#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BIWENGER LIGA MANAGER
Aplicación para gestionar ligas de Biwenger
Versión: 1.0 - Completa
"""

import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
from datetime import datetime, timedelta
import webbrowser
import json
import os

# Configurar ruta de datos
try:
    from kivy.utils import platform
    if platform == 'android':
        from android.storage import primary_external_storage_path
        DATA_DIR = os.path.join(primary_external_storage_path(), 'BiwengerLiga')
    else:
        DATA_DIR = os.path.expanduser('~/.biwenger_liga')
except:
    DATA_DIR = os.path.expanduser('~/.biwenger_liga')

# Crear directorio si no existe
os.makedirs(DATA_DIR, exist_ok=True)

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'login'
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # Logo/Título
        title = Label(
            text='⚽ BIWENGER LIGA MANAGER ⚽', 
            font_size='28sp', 
            size_hint_y=0.3,
            color=[0, 0.8, 0, 1]
        )
        main_layout.add_widget(title)
        
        # Formulario de login
        form_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.4)
        
        self.username = TextInput(
            hint_text='👤 Usuario', 
            multiline=False, 
            size_hint_y=None,
            height='48dp',
            font_size='16sp'
        )
        form_layout.add_widget(self.username)
        
        self.password = TextInput(
            hint_text='🔒 Contraseña', 
            password=True, 
            multiline=False,
            size_hint_y=None,
            height='48dp',
            font_size='16sp'
        )
        form_layout.add_widget(self.password)
        
        main_layout.add_widget(form_layout)
        
        # Botones
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        login_btn = Button(
            text='🚀 ENTRAR',
            font_size='18sp',
            background_color=[0, 0.7, 0, 1]
        )
        login_btn.bind(on_press=self.login)
        btn_layout.add_widget(login_btn)
        
        register_btn = Button(
            text='📝 REGISTRO',
            font_size='18sp',
            background_color=[0, 0.5, 0.8, 1]
        )
        register_btn.bind(on_press=self.register)
        btn_layout.add_widget(register_btn)
        
        main_layout.add_widget(btn_layout)
        
        # Info de administrador
        info_label = Label(
            text='👑 Admin por defecto: admin / admin123',
            size_hint_y=0.1,
            font_size='14sp',
            color=[0.7, 0.7, 0.7, 1]
        )
        main_layout.add_widget(info_label)
        
        self.add_widget(main_layout)
    
    def login(self, instance):
        if not self.username.text or not self.password.text:
            self.show_popup('❌ Error', 'Por favor, completa todos los campos')
            return
            
        app = App.get_running_app()
        if app.verify_login(self.username.text, self.password.text):
            self.username.text = ''
            self.password.text = ''
            app.root.current = 'main'
        else:
            self.show_popup('❌ Error', 'Usuario o contraseña incorrectos')
    
    def register(self, instance):
        App.get_running_app().root.current = 'register'
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'register'
        
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        title = Label(
            text='📝 REGISTRO NUEVO JUGADOR', 
            font_size='24sp', 
            size_hint_y=0.15,
            color=[0, 0.8, 0, 1]
        )
        main_layout.add_widget(title)
        
        scroll = ScrollView(size_hint_y=0.65)
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        self.username = TextInput(
            hint_text='👤 Usuario (obligatorio)', 
            multiline=False,
            size_hint_y=None,
            height='48dp'
        )
        form_layout.add_widget(self.username)
        
        self.password = TextInput(
            hint_text='🔒 Contraseña (obligatorio)', 
            password=True, 
            multiline=False,
            size_hint_y=None,
            height='48dp'
        )
        form_layout.add_widget(self.password)
        
        self.email = TextInput(
            hint_text='📧 Email', 
            multiline=False,
            size_hint_y=None,
            height='48dp'
        )
        form_layout.add_widget(self.email)
        
        self.phone = TextInput(
            hint_text='📱 Teléfono (para WhatsApp)', 
            multiline=False,
            size_hint_y=None,
            height='48dp'
        )
        form_layout.add_widget(self.phone)
        
        self.biwenger_user = TextInput(
            hint_text='⚽ Usuario Biwenger', 
            multiline=False,
            size_hint_y=None,
            height='48dp'
        )
        form_layout.add_widget(self.biwenger_user)
        
        scroll.add_widget(form_layout)
        main_layout.add_widget(scroll)
        
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        register_btn = Button(
            text='✅ REGISTRARSE',
            background_color=[0, 0.7, 0, 1],
            font_size='16sp'
        )
        register_btn.bind(on_press=self.register_user)
        btn_layout.add_widget(register_btn)
        
        back_btn = Button(
            text='🔙 VOLVER',
            background_color=[0.7, 0.7, 0.7, 1],
            font_size='16sp'
        )
        back_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(back_btn)
        
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)
    
    def register_user(self, instance):
        if not self.username.text or not self.password.text:
            self.show_popup('❌ Error', 'Usuario y contraseña son obligatorios')
            return
            
        app = App.get_running_app()
        result = app.register_user(
            self.username.text, 
            self.password.text, 
            self.email.text, 
            self.phone.text, 
            self.biwenger_user.text
        )
        
        if result == "success":
            self.clear_form()
            self.show_popup('✅ Éxito', 'Usuario registrado correctamente')
            Clock.schedule_once(lambda dt: setattr(app.root, 'current', 'login'), 1.5)
        elif result == "exists":
            self.show_popup('❌ Error', 'El usuario ya existe')
        else:
            self.show_popup('❌ Error', 'No se pudo registrar el usuario')
    
    def clear_form(self):
        self.username.text = ''
        self.password.text = ''
        self.email.text = ''
        self.phone.text = ''
        self.biwenger_user.text = ''
    
    def go_back(self, instance):
        App.get_running_app().root.current = 'login'
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'main'
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = BoxLayout(size_hint_y=0.15, spacing=10)
        
        self.user_label = Label(
            text='👋 Bienvenido', 
            font_size='20sp',
            color=[0, 0.8, 0, 1]
        )
        header.add_widget(self.user_label)
        
        logout_btn = Button(
            text='🚪 SALIR', 
            size_hint_x=0.3,
            background_color=[0.8, 0.2, 0.2, 1],
            font_size='16sp'
        )
        logout_btn.bind(on_press=self.logout)
        header.add_widget(logout_btn)
        
        main_layout.add_widget(header)
        
        buttons_scroll = ScrollView(size_hint_y=0.85)
        buttons_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        
        menu_items = [
            ('⚽ BIWENGER', [0, 0.6, 0.8, 1], self.go_to_biwenger),
            ('🚨 SANCIONES', [0.8, 0.4, 0, 1], self.go_to_sanctions),
            ('🏆 PREMIOS', [0.8, 0.6, 0, 1], self.go_to_prizes),
            ('💰 DINERO', [0, 0.8, 0.4, 1], self.show_sanctions_money),
            ('💬 WHATSAPP', [0.2, 0.8, 0.2, 1], self.open_whatsapp),
            ('📋 REGLAS', [0.6, 0.6, 0.6, 1], self.show_rules),
            ('👤 MI PERFIL', [0.5, 0.3, 0.8, 1], self.show_profile),
            ('⚙️ CONFIGURACIÓN', [0.3, 0.3, 0.3, 1], self.show_settings)
        ]
        
        for text, color, callback in menu_items:
            btn = Button(
                text=text,
                background_color=color,
                font_size='16sp',
                size_hint_y=None,
                height='80dp'
            )
            btn.bind(on_press=callback)
            buttons_layout.add_widget(btn)
        
        buttons_scroll.add_widget(buttons_layout)
        main_layout.add_widget(buttons_scroll)
        
        self.add_widget(main_layout)
    
    def on_enter(self):
        app = App.get_running_app()
        if app.current_user:
            is_admin = " (ADMIN)" if app.is_admin() else ""
            self.user_label.text = f'👋 Hola {app.current_user}{is_admin}'
    
    def logout(self, instance):
        app = App.get_running_app()
        app.current_user = None
        app.root.current = 'login'
    
    def go_to_biwenger(self, instance):
        App.get_running_app().root.current = 'biwenger'
    
    def go_to_sanctions(self, instance):
        App.get_running_app().root.current = 'sanctions'
    
    def go_to_prizes(self, instance):
        App.get_running_app().root.current = 'prizes'
    
    def show_sanctions_money(self, instance):
        app = App.get_running_app()
        total = app.calculate_sanctions_money()
        self.show_popup('💰 Dinero de Sanciones', f'Total acumulado: {total:.2f}€')
    
    def open_whatsapp(self, instance):
        app = App.get_running_app()
        app.create_whatsapp_group()
    
    def show_profile(self, instance):
        App.get_running_app().root.current = 'profile'
    
    def show_settings(self, instance):
        if App.get_running_app().is_admin():
            App.get_running_app().root.current = 'settings'
        else:
            self.show_popup('❌ Acceso denegado', 'Solo el administrador puede acceder a la configuración')
    
    def show_rules(self, instance):
        App.get_running_app().root.current = 'rules'
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class BiwengerScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'biwenger'
        
        main_layout = BoxLayout(orientation='vertical', padding=15, spacing=15)
        
        title = Label(
            text='⚽ GESTIÓN BIWENGER', 
            font_size='24sp', 
            size_hint_y=0.2,
            color=[0, 0.8, 0, 1]
        )
        main_layout.add_widget(title)
        
        buttons_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=0.6)
        
        signup_btn = Button(
            text='🔗 REGISTRARSE EN BIWENGER',
            font_size='18sp',
            background_color=[0, 0.7, 0, 1]
        )
        signup_btn.bind(on_press=self.signup_biwenger)
        buttons_layout.add_widget(signup_btn)
        
        lineup_btn = Button(
            text='👥 VER ALINEACIONES',
            font_size='18sp',
            background_color=[0, 0.5, 0.8, 1]
        )
        lineup_btn.bind(on_press=self.view_lineups)
        buttons_layout.add_widget(lineup_btn)
        
        transfers_btn = Button(
            text='🔄 GESTIÓN FICHAJES',
            font_size='18sp',
            background_color=[0.8, 0.5, 0, 1]
        )
        transfers_btn.bind(on_press=self.manage_transfers)
        buttons_layout.add_widget(transfers_btn)
        
        main_layout.add_widget(buttons_layout)
        
        back_btn = Button(
            text='🔙 VOLVER AL MENÚ',
            size_hint_y=0.2,
            background_color=[0.7, 0.7, 0.7, 1],
            font_size='16sp'
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def signup_biwenger(self, instance):
        try:
            webbrowser.open('https://www.biwenger.com/auth/register')
            self.show_popup('🔗 Biwenger', '¡Abriendo página de registro!\n\nRegístrate y luego vuelve a la app')
        except:
            self.show_popup('❌ Error', 'No se pudo abrir el navegador')
    
    def view_lineups(self, instance):
        self.show_popup('👥 Alineaciones', '🚧 Próximamente...\n\nSe conectará con la API de Biwenger para mostrar todas las alineaciones de la liga')
    
    def manage_transfers(self, instance):
        self.show_popup('🔄 Fichajes', '🚧 Próximamente...\n\nPodrás ver y gestionar todos los fichajes de la liga desde aquí')
    
    def go_back(self, instance):
        App.get_running_app().root.current = 'main'
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title, 
            content=Label(text=message, text_size=(350, None), halign='center'),
            size_hint=(0.85, 0.5)
        )
        popup.open()

class SanctionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'sanctions'
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        header = BoxLayout(size_hint_y=0.15, spacing=10)
        
        title = Label(
            text='🚨 GESTIÓN SANCIONES', 
            font_size='20sp',
            color=[0.8, 0.4, 0, 1]
        )
        header.add_widget(title)
        
        self.summary_label = Label(
            text='💰 Total: 0.00€',
            font_size='16sp',
            size_hint_x=0.4,
            color=[0, 0.8, 0, 1]
        )
        header.add_widget(self.summary_label)
        
        main_layout.add_widget(header)
        
        scroll = ScrollView(size_hint_y=0.65)
        self.players_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.players_layout.bind(minimum_height=self.players_layout.setter('height'))
        scroll.add_widget(self.players_layout)
        main_layout.add_widget(scroll)
        
        controls_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        app = App.get_running_app()
        if app.is_admin():
            add_sanction_btn = Button(
                text='➕ AÑADIR SANCIÓN',
                background_color=[0.8, 0.4, 0, 1]
            )
            add_sanction_btn.bind(on_press=self.add_sanction)
            controls_layout.add_widget(add_sanction_btn)
        
        refresh_btn = Button(
            text='🔄 ACTUALIZAR',
            background_color=[0, 0.7, 0, 1]
        )
        refresh_btn.bind(on_press=lambda x: self.update_players_list())
        controls_layout.add_widget(refresh_btn)
        
        back_btn = Button(
            text='🔙 VOLVER',
            background_color=[0.7, 0.7, 0.7, 1]
        )
        back_btn.bind(on_press=self.go_back)
        controls_layout.add_widget(back_btn)
        
        main_layout.add_widget(controls_layout)
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.update_players_list()
    
    def update_players_list(self):
        self.players_layout.clear_widgets()
        app = App.get_running_app()
        
        total_sanctions = app.calculate_sanctions_money()
        self.summary_label.text = f'💰 Total: {total_sanctions:.2f}€'
        
        players = app.get_all_players()
        if not players:
            no_players = Label(
                text='👥 No hay jugadores registrados',
                size_hint_y=None,
                height='60dp'
            )
            self.players_layout.add_widget(no_players)
            return
        
        for player in players:
            player_layout = BoxLayout(size_hint_y=None, height='70dp', spacing=10)
            
            sanctions_text = f"{player.get('sanctions', 0):.2f}€"
            status_emoji = "🚨" if player.get('sanctions', 0) > 0 else "✅"
            
            player_info = Label(
                text=f"{status_emoji} {player['username']}\nSanciones: {sanctions_text}",
                size_hint_x=0.6,
                text_size=(None, None),
                halign='left'
            )
            player_layout.add_widget(player_info)
            
            if app.is_admin() and player['username'] != app.current_user:
                btn_layout = BoxLayout(size_hint_x=0.4, spacing=5)
                
                pay_btn = Button(
                    text='💰',
                    size_hint_x=0.5,
                    background_color=[0, 0.8, 0, 1]
                )
                pay_btn.bind(on_press=lambda x, p=player: self.pay_sanction(p))
                btn_layout.add_widget(pay_btn)
                
                edit_btn = Button(
                    text='✏️',
                    size_hint_x=0.5,
                    background_color=[0.8, 0.6, 0.2, 1]
                )
                edit_btn.bind(on_press=lambda x, p=player: self.edit_player(p))
                btn_layout.add_widget(edit_btn)
                
                player_layout.add_widget(btn_layout)
            
            self.players_layout.add_widget(player_layout)
    
    def add_sanction(self, instance):
        if not App.get_running_app().is_admin():
            self.show_popup('❌ Error', 'Solo el administrador puede añadir sanciones')
            return
        
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        player_input = TextInput(
            hint_text='👤 Usuario del jugador', 
            multiline=False,
            size_hint_y=None,
            height='48dp'
        )
        content.add_widget(player_input)
        
        sanctions_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height='120dp')
        
        predefined_sanctions = [
            ('Saldo negativo', 10),
            ('Alineación indebida', 5),
            ('No pago inicial', 20),
            ('Reincidencia', 15)
        ]
        
        popup = Popup(
            title='➕ Añadir Sanción',
            content=content,
            size_hint=(0.9, 0.7)
        )
        
        for text, amount in predefined_sanctions:
            btn = Button(text=f'{text}\n{amount}€', font_size='12sp')
            btn.bind(on_press=lambda x, a=amount, t=text: self.add_predefined_sanction(
                player_input.text, a, t, popup
            ))
           