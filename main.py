#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
from kivy.storage.jsonstore import JsonStore
from kivy.clock import Clock
from datetime import datetime, timedelta
import webbrowser
import json
import os

# Configurar ruta de datos
if hasattr(App.get_running_app, '__call__'):
    try:
        DATA_DIR = App.get_running_app().user_data_dir
    except:
        DATA_DIR = os.path.expanduser('~')
else:
    DATA_DIR = os.path.expanduser('~')

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
            color=[0, 0.8, 0, 1]  # Verde
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
            # Limpiar campos
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
        
        # Título
        title = Label(
            text='📝 REGISTRO NUEVO JUGADOR', 
            font_size='24sp', 
            size_hint_y=0.15,
            color=[0, 0.8, 0, 1]
        )
        main_layout.add_widget(title)
        
        # Scroll para formulario
        scroll = ScrollView(size_hint_y=0.65)
        form_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Campos del formulario
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
        
        # Botones
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
        
        if result:
            self.show_popup('✅ Éxito', 'Usuario registrado correctamente')
            Clock.schedule_once(lambda dt: setattr(app.root, 'current', 'login'), 1.5)
        else:
            self.show_popup('❌ Error', 'El usuario ya existe')
    
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
        
        # Header
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
        
        # Grid de botones principales
        buttons_scroll = ScrollView(size_hint_y=0.85)
        buttons_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        buttons_layout.bind(minimum_height=buttons_layout.setter('height'))
        
        # Botones del menú
        menu_items = [
            ('⚽ BIWENGER', [0, 0.6, 0.8, 1], self.go_to_biwenger),
            ('🚨 SANCIONES', [0.8, 0.4, 0, 1], self.go_to_sanctions),
            ('🏆 PREMIOS', [0.8, 0.6, 0, 1], self.go_to_prizes),
            ('💰 DINERO', [0, 0.8, 0.4, 1], self.show_sanctions_money),
            ('💬 WHATSAPP', [0.2, 0.8, 0.2, 1], self.open_whatsapp),
            ('📋 REGLAS', [0.6, 0.6, 0.6, 1], self.show_rules)
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
        
        # Título
        title = Label(
            text='⚽ GESTIÓN BIWENGER', 
            font_size='24sp', 
            size_hint_y=0.2,
            color=[0, 0.8, 0, 1]
        )
        main_layout.add_widget(title)
        
        # Botones de gestión
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
        
        # Botón volver
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
        webbrowser.open('https://www.biwenger.com/auth/register')
        self.show_popup('🔗 Biwenger', '¡Abriendo página de registro!\n\nRegístrate y luego vuelve a la app')
    
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
        
        # Header
        header = BoxLayout(size_hint_y=0.15, spacing=10)
        
        title = Label(
            text='🚨 GESTIÓN SANCIONES', 
            font_size='20sp',
            color=[0.8, 0.4, 0, 1]
        )
        header.add_widget(title)
        
        # Resumen de sanciones
        app = App.get_running_app()
        total_sanctions = app.calculate_sanctions_money()
        summary = Label(
            text=f'💰 Total: {total_sanctions:.2f}€',
            font_size='16sp',
            size_hint_x=0.4,
            color=[0, 0.8, 0, 1]
        )
        header.add_widget(summary)
        
        main_layout.add_widget(header)
        
        # Lista de jugadores
        scroll = ScrollView(size_hint_y=0.65)
        self.players_layout = GridLayout(cols=1, size_hint_y=None, spacing=5)
        self.players_layout.bind(minimum_height=self.players_layout.setter('height'))
        scroll.add_widget(self.players_layout)
        main_layout.add_widget(scroll)
        
        # Botones de control
        controls_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
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
            
            # Info del jugador
            sanctions_text = f"{player.get('sanctions', 0):.2f}€"
            status_emoji = "🚨" if player.get('sanctions', 0) > 0 else "✅"
            
            player_info = Label(
                text=f"{status_emoji} {player['username']}\nSanciones: {sanctions_text}",
                size_hint_x=0.6,
                text_size=(None, None),
                halign='left'
            )
            player_layout.add_widget(player_info)
            
            # Botones de admin
            if app.is_admin() and player['username'] != app.current_user:
                btn_layout = BoxLayout(size_hint_x=0.4, spacing=5)
                
                pay_btn = Button(
                    text='💰',
                    size_hint_x=0.5,
                    background_color=[0, 0.8, 0, 1]
                )
                pay_btn.bind(on_press=lambda x, p=player: self.pay_sanction(p))
                btn_layout.add_widget(pay_btn)
                
                remove_btn = Button(
                    text='❌',
                    size_hint_x=0.5,
                    background_color=[0.8, 0.2, 0.2, 1]
                )
                remove_btn.bind(on_press=lambda x, p=player: self.remove_player(p))
                btn_layout.add_widget(remove_btn)
                
                player_layout.add_widget(btn_layout)
            
            self.players_layout.add_widget(player_layout)
    
    def add_sanction(self, instance):
        if not App.get_running_app().is_admin():
            self.show_popup('❌ Error', 'Solo el administrador puede añadir sanciones')
            return
        
        # Crear popup para añadir sanción
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        player_input = TextInput(
            hint_text='👤 Usuario del jugador', 
            multiline=False,
            size_hint_y=None,
            height='48dp'
        )
        content.add_widget(player_input)
        
        # Botones de sanciones predefinidas
        sanctions_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height='120dp')
        
        predefined_sanctions = [
            ('Saldo negativo', 10),
            ('Alineación indebida', 5),
            ('No pago inicial', 20),
            ('Reincidencia', 15)
        ]
        
        for text, amount in predefined_sanctions:
            btn = Button(text=f'{text}\n{amount}€', font_size='12sp')
            btn.bind(on_press=lambda x, a=amount, t=text: self.add_predefined_sanction(
                player_input.text, a, t, popup
            ))
            sanctions_layout.add_widget(btn)
        
        content.add_widget(sanctions_layout)
        
        # Sanción personalizada
        custom_layout = BoxLayout(spacing=10, size_hint_y=None, height='48dp')
        sanction_input = TextInput(
            hint_text='💰 Cantidad personalizada (€)', 
            multiline=False
        )
        custom_layout.add_widget(sanction_input)
        
        custom_btn = Button(text='➕', size_hint_x=0.2)
        custom_btn.bind(on_press=lambda x: self.add_custom_sanction(
            player_input.text, sanction_input.text, popup
        ))
        custom_layout.add_widget(custom_btn)
        
        content.add_widget(custom_layout)
        
        # Botón cancelar
        cancel_btn = Button(
            text='❌ CANCELAR',
            size_hint_y=None,
            height='48dp',
            background_color=[0.7, 0.7, 0.7, 1]
        )
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        content.add_widget(cancel_btn)
        
        popup = Popup(
            title='➕ Añadir Sanción',
            content=content,
            size_hint=(0.9, 0.7)
        )
        popup.open()
    
    def add_predefined_sanction(self, username, amount, reason, popup):
        if not username:
            self.show_popup('❌ Error', 'Introduce el nombre del jugador')
            return
        
        app = App.get_running_app()
        if app.add_sanction(username, amount, reason):
            self.show_popup('✅ Éxito', f'Sanción de {amount}€ añadida a {username}')
            self.update_players_list()
            popup.dismiss()
        else:
            self.show_popup('❌ Error', 'Jugador no encontrado')
    
    def add_custom_sanction(self, username, amount_str, popup):
        if not username or not amount_str:
            self.show_popup('❌ Error', 'Completa todos los campos')
            return
        
        try:
            amount = float(amount_str)
            app = App.get_running_app()
            if app.add_sanction(username, amount, 'Sanción personalizada'):
                self.show_popup('✅ Éxito', f'Sanción de {amount}€ añadida a {username}')
                self.update_players_list()
                popup.dismiss()
            else:
                self.show_popup('❌ Error', 'Jugador no encontrado')
        except ValueError:
            self.show_popup('❌ Error', 'Cantidad inválida')
    
    def pay_sanction(self, player):
        app = App.get_running_app()
        if app.pay_sanction(player['username']):
            self.show_popup('✅ Pagado', f'Sanciones de {player["username"]} pagadas')
            self.update_players_list()
    
    def remove_player(self, player):
        app = App.get_running_app()
        
        # Confirmación
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=f'¿Expulsar a {player["username"]}?'))
        
        btn_layout = BoxLayout(spacing=10)
        
        confirm_btn = Button(text='✅ SÍ', background_color=[0.8, 0.2, 0.2, 1])
        cancel_btn = Button(text='❌ NO', background_color=[0.7, 0.7, 0.7, 1])
        
        btn_layout.add_widget(confirm_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title='⚠️ Confirmar Expulsión', content=content, size_hint=(0.8, 0.4))
        
        def confirm_removal(instance):
            if app.remove_player(player['username']):
                self.show_popup('✅ Expulsado', f'{player["username"]} ha sido expulsado')
                self.update_players_list()
            popup.dismiss()
        
        confirm_btn.bind(on_press=confirm_removal)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        App.get_running_app().root.current = 'main'
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class PrizesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'prizes'
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='🏆 PREMIOS ECONÓMICOS',
            font_size='24sp', 
            size_hint_y=0.15,
            color=[0.8, 0.6, 0, 1]
        )
        main_layout.add_widget(title)
        
        # Información de premios
        scroll = ScrollView(size_hint_y=0.65)
        self.prizes_layout = GridLayout(cols=1, size_hint_y=None, spacing=10, padding=10)
        self.prizes_layout.bind(minimum_height=self.prizes_layout.setter('height'))
        scroll.add_widget(self.prizes_layout)
        main_layout.add_widget(scroll)
        
        # Botones
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        app = App.get_running_app()
        if app.is_admin():
            modify_btn = Button(
                text='✏️ MODIFICAR PREMIOS',
                background_color=[0.8, 0.6, 0, 1],
                font_size='16sp'
            )
            modify_btn.bind(on_press=self.modify_prizes)
            btn_layout.add_widget(modify_btn)
        
        refresh_btn = Button(
            text='🔄 ACTUALIZAR',
            background_color=[0, 0.7, 0, 1],
            font_size='16sp'
        )
        refresh_btn.bind(on_press=lambda x: self.update_prizes_list())
        btn_layout.add_widget(refresh_btn)
        
        back_btn = Button(
            text='🔙 VOLVER',
            background_color=[0.7, 0.7, 0.7, 1],
            font_size='16sp'
        )
        back_btn.bind(on_press=self.go_back)
        btn_layout.add_widget(back_btn)
        
        main_layout.add_widget(btn_layout)
        self.add_widget(main_layout)
    
    def on_enter(self):
        self.update_prizes_list()
    
    def update_prizes_list(self):
        self.prizes_layout.clear_widgets()
        app = App.get_running_app()
        prizes = app.get_prizes()
        
        # Explicación del sistema
        explanation = Label(
            text='💡 Sistema de premios invertido para fomentar las remontadas:\nDel último al primero, más dinero por posición',
            size_hint_y=None,
            height='60dp',
            color=[0, 0.8, 0, 1],
            font_size='14sp'
        )
        self.prizes_layout.add_widget(explanation)
        
        # Lista de premios ordenados
        sorted_prizes = sorted(prizes.items(), key=lambda x: int(x[0]))
        
        for position, amount in sorted_prizes:
            # Determinar emoji según posición
            if position == '1':
                emoji = '🥇'
            elif position == '2':
                emoji = '🥈'
            elif position == '3':
                emoji = '🥉'
            else:
                emoji = f'#{position}'
            
            prize_layout = BoxLayout(size_hint_y=None, height='50dp', spacing=10)
            
            prize_label = Label(
                text=f'{emoji} Puesto {position}°',
                size_hint_x=0.4,
                font_size='16sp'
            )
            prize_layout.add_widget(prize_label)
            
            amount_label = Label(
                text=f'{amount:,.0f}€',
                size_hint_x=0.6,
                font_size='18sp',
                color=[0, 0.8, 0, 1]
            )
            prize_layout.add_widget(amount_label)
            
            self.prizes_layout.add_widget(prize_layout)
    
    def modify_prizes(self, instance):
        if not App.get_running_app().is_admin():
            self.show_popup('❌ Error', 'Solo el administrador puede modificar premios')
            return
        
        # Popup para modificar premios
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        content.add_widget(Label(
            text='✏️ Modificar Premios\nIntroduce los nuevos valores:',
            size_hint_y=None,
            height='60dp'
        ))
        
        # Scroll para los inputs
        scroll = ScrollView(size_hint_y=0.7)
        inputs_layout = GridLayout(cols=2, size_hint_y=None, spacing=10)
        inputs_layout.bind(minimum_height=inputs_layout.setter('height'))
        
        app = App.get_running_app()
        prizes = app.get_prizes()
        prize_inputs = {}
        
        for position in sorted(prizes.keys(), key=int):
            # Label de posición
            pos_label = Label(
                text=f'🏆 Puesto {position}°:',
                size_hint_y=None,
                height='40dp'
            )
            inputs_layout.add_widget(pos_label)
            
            # Input para el premio
            prize_input = TextInput(
                text=str(prizes[position]),
                multiline=False,
                size_hint_y=None,
                height='40dp',
                input_filter='int'
            )
            prize_inputs[position] = prize_input
            inputs_layout.add_widget(prize_input)
        
        scroll.add_widget(inputs_layout)
        content.add_widget(scroll)
        
        # Botones
        btn_layout = BoxLayout(size_hint_y=0.2, spacing=10)
        
        save_btn = Button(
            text='💾 GUARDAR',
            background_color=[0, 0.7, 0, 1]
        )
        cancel_btn = Button(
            text='❌ CANCELAR',
            background_color=[0.7, 0.7, 0.7, 1]
        )
        
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)
        content.add_widget(btn_layout)
        
        popup = Popup(title='✏️ Modificar Premios', content=content, size_hint=(0.9, 0.8))
        
        def save_prizes(instance):
            try:
                new_prizes = {}
                for pos, input_widget in prize_inputs.items():
                    new_prizes[pos] = int(input_widget.text)
                
                app.update_prizes(new_prizes)
                self.show_popup('💾 Guardado', 'Premios actualizados correctamente')
                self.update_prizes_list()
                popup.dismiss()
            except ValueError:
                self.show_popup('❌ Error', 'Introduce solo números válidos')
        
        save_btn.bind(on_press=save_prizes)
        cancel_btn.bind(on_press=popup.dismiss)
        popup.open()
    
    def go_back(self, instance):
        App.get_running_app().root.current = 'main'
    
    def show_popup(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message, text_size=(300, None), halign='center'),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class RulesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'rules'
        
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='📋 REGLAS DE LA LIGA',
            font_size='24sp',
            size_hint_y=0.15,
            color=[0.6, 0.6, 0.6, 1]
        )
        main_layout.add_widget(title)
        
        # Reglas en scroll
        scroll = ScrollView(size_hint_y=0.75)
        
        rules_text = """
🏆 LIGA BIWENGER - REGLAS OFICIALES

💰 SANCIONES ECONÓMICAS:

🔸 Inscripción Obligatoria:
   • 20€ antes de empezar a jugar
   • Sin pago = EXPULSIÓN inmediata

🔸 Saldo Negativo:
   • 1ª vez: 10€ de sanción
   • 2ª vez sin pagar: 15€ adicionales
   • 3ª jornada sin pagar: EXPULSIÓN

🔸 Alineación Indebida:
   • Falta de jugadores: 5€ de sanción
   • 3ª jornada sin pagar: EXPULSIÓN

🏆 PREMIOS ECONÓMICOS:

Sistema invertido para fomentar remontadas:
• 🥇 1º puesto: 1.000.000€
• 🥈 2º puesto: 1.500.000€
• 🥉 3º puesto: 2.000.000€
• 4º puesto: 2.500.000€
• 5º puesto: 3.000.000€
• Y así sucesivamente...

⚖️ ADMINISTRACIÓN:

🔸 El administrador puede:
   • Modificar reglas y premios
   • Añadir/quitar sanciones
   • Expulsar jugadores
   • Gestionar el dinero de sanciones

🔸 Transparencia total:
   • Todas las sanciones son visibles
   • Registro de todas las acciones
   • Chat grupal para comunicación

📱 FUNCIONALIDADES:

🔸 Integración Biwenger:
   • Registro directo
   • Visualización de alineaciones
   • Gestión de fichajes

🔸 Comunicación:
   • Chat de WhatsApp integrado
   • Notificaciones de sanciones
   • Actualizaciones en tiempo real

⚠️ IMPORTANTE:

• Todas las reglas pueden ser modificadas por el admin
• Las sanciones son acumulativas
• El dinero de sanciones se suma al bote final
• Fair play y respeto entre todos los participantes

🎮 ¡QUE COMIENCE LA COMPETICIÓN!
        """
        
        rules_label = Label(
            text=rules_text,
            text_size=(None, None),
            valign='top',
            halign='left',
            font_size='13sp'
        )
        scroll.add_widget(rules_label)
        main_layout.add_widget(scroll)
        
        # Botón volver
        back_btn = Button(
            text='🔙 VOLVER AL MENÚ',
            size_hint_y=0.1,
            background_color=[0.7, 0.7, 0.7, 1],
            font_size='16sp'
        )
        back_btn.bind(on_press=self.go_back)
        main_layout.add_widget(back_btn)
        
        self.add_widget(main_layout)
    
    def go_back(self, instance):
        App.get_running_app().root.current = 'main'

class BiwengerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Biwenger Liga Manager'
        
        # Configurar almacenamiento
        try:
            data_path = os.path.join(self.user_data_dir, 'biwenger_data.json')
        except:
            data_path = 'biwenger_data.json'
        
        self.store = JsonStore(data_path)
        self.current_user = None
        self.admin_user = 'admin'
        
        # Inicializar datos
        self.init_default_data()
    
    def init_default_data(self):
        """Inicializar datos por defecto"""
        if not self.store.exists('users'):
            self.store.put('users', admin={
                'password': 'admin123',
                'email': 'admin@biwenger.com',
                'phone': '+34600000000',
                'biwenger_user': 'admin_biwenger',
                'sanctions': 0,
                'is_admin': True,
                'registration_date': datetime.now().isoformat()
            })
        
        if not self.store.exists('prizes'):
            default_prizes = {}
            base_prize = 1000000
            for i in range(1, 13):  # Hasta 12 jugadores
                default_prizes[str(i)] = base_prize + (i-1) * 500000
            
            self.store.put('prizes', **default_prizes)
        
        if not self.store.exists('sanctions_history'):
            self.store.put('sanctions_history', history=[])
    
    def build(self):
        """Construir la aplicación"""
        sm = ScreenManager()
        
        # Añadir todas las pantallas
        sm.add_widget(LoginScreen())
        sm.add_widget(RegisterScreen())
        sm.add_widget(MainScreen())
        sm.add_widget(BiwengerScreen())
        sm.add_widget(SanctionsScreen())
        sm.add_widget(PrizesScreen())
        sm.add_widget(RulesScreen())
        
        return sm
    
    def verify_login(self, username, password):
        """Verificar credenciales de login"""
        if self.store.exists('users'):
            users = self.store.get('users')
            if username in users and users[username]['password'] == password:
                self.current_user = username
                return True
        return False
    
    def register_user(self, username, password, email, phone, biwenger_user):
        """Registrar nuevo usuario"""
        if not username or not password:
            return False
        
        users = self.store.get('users') if self.store.exists('users') else {}
        
        # Verificar si ya existe
        if username in users:
            return False
        
        # Añadir nuevo usuario
        users[username] = {
            'password': password,
            'email': email,
            'phone': phone,
            'biwenger_user': biwenger_user,
            'sanctions': 0,
            'is_admin': False,
            'registration_date': datetime.now().isoformat()
        }
        
        self.store.put('users', **users)
        return True
    
    def is_admin(self):
        """Verificar si el usuario actual es admin"""
        if not self.current_user:
            return False
        
        if not self.store.exists('users'):
            return False
        
        users = self.store.get('users')
        return users.get(self.current_user, {}).get('is_admin', False)
    
    def get_all_players(self):
        """Obtener lista de todos los jugadores"""
        if not self.store.exists('users'):
            return []
        
        users = self.store.get('users')
        players = []
        
        for username, data in users.items():
            players.append({
                'username': username,
                'sanctions': data.get('sanctions', 0),
                'phone': data.get('phone', ''),
                'email': data.get('email', ''),
                'biwenger_user': data.get('biwenger_user', ''),
                'is_admin': data.get('is_admin', False)
            })
        
        return sorted(players, key=lambda x: x['sanctions'], reverse=True)
    
    def add_sanction(self, username, amount, reason):
        """Añadir sanción a un jugador"""
        if not self.is_admin():
            return False
        
        if not self.store.exists('users'):
            return False
        
        users = self.store.get('users')
        if username not in users:
            return False
        
        # Añadir sanción
        users[username]['sanctions'] = users[username].get('sanctions', 0) + amount
        self.store.put('users', **users)
        
        # Registrar en historial
        self.add_to_sanctions_history(username, amount, reason)
        
        return True
    
    def pay_sanction(self, username):
        """Pagar todas las sanciones de un jugador"""
        if not self.is_admin():
            return False
        
        if not self.store.exists('users'):
            return False
        
        users = self.store.get('users')
        if username not in users:
            return False
        
        # Resetear sanciones
        old_amount = users[username].get('sanctions', 0)
        users[username]['sanctions'] = 0
        self.store.put('users', **users)
        
        # Registrar pago en historial
        self.add_to_sanctions_history(username, -old_amount, 'Pago de sanciones')
        
        return True
    
    def remove_player(self, username):
        """Expulsar jugador"""
        if not self.is_admin() or username == self.admin_user:
            return False
        
        if not self.store.exists('users'):
            return False
        
        users = self.store.get('users')
        if username in users:
            del users[username]
            self.store.put('users', **users)
            
            # Registrar expulsión
            self.add_to_sanctions_history(username, 0, 'EXPULSADO de la liga')
            return True
        
        return False
    
    def calculate_sanctions_money(self):
        """Calcular dinero total de sanciones"""
        if not self.store.exists('users'):
            return 0.0
        
        users = self.store.get('users')
        total = sum(user.get('sanctions', 0) for user in users.values())
        return float(total)
    
    def get_prizes(self):
        """Obtener configuración de premios"""
        if self.store.exists('prizes'):
            return self.store.get('prizes')
        return {}
    
    def update_prizes(self, new_prizes):
        """Actualizar premios (solo admin)"""
        if not self.is_admin():
            return False
        
        self.store.put('prizes', **new_prizes)
        return True
    
    def add_to_sanctions_history(self, username, amount, reason):
        """Añadir entrada al historial de sanciones"""
        history = self.store.get('sanctions_history')['history'] if self.store.exists('sanctions_history') else []
        
        entry = {
            'username': username,
            'amount': amount,
            'reason': reason,
            'date': datetime.now().isoformat(),
            'admin': self.current_user
        }
        
        history.append(entry)
        self.store.put('sanctions_history', history=history)
    
    def create_whatsapp_group(self):
        """Crear enlace para grupo de WhatsApp"""
        players = self.get_all_players()
        active_players = [p for p in players if p['phone']]
        
        if not active_players:
            # Mostrar popup si no hay teléfonos
            popup = Popup(
                title='📱 WhatsApp',
                content=Label(
                    text='❌ No hay números registrados\n\nPide a los jugadores que actualicen sus perfiles con su número de teléfono',
                    text_size=(300, None),
                    halign='center'
                ),
                size_hint=(0.8, 0.5)
            )
            popup.open()
            return
        
        # Crear mensaje para el grupo
        group_name = "🏆 Liga Biwenger"
        message = f"¡Únete a {group_name}! Gestiona tu participación desde la app Biwenger Liga Manager"
        
        # Abrir WhatsApp
        try:
            whatsapp_url = f"https://wa.me/?text={message.replace(' ', '%20')}"
            webbrowser.open(whatsapp_url)
            
            # Mostrar confirmación
            popup = Popup(
                title='💬 WhatsApp',
                content=Label(
                    text=f'✅ ¡Abriendo WhatsApp!\n\nJugadores con teléfono: {len(active_players)}\n\nCrea el grupo y comparte el enlace',
                    text_size=(300, None),
                    halign='center'
                ),
                size_hint=(0.8, 0.5)
            )
            popup.open()
            
        except Exception as e:
            popup = Popup(
                title='❌ Error',
                content=Label(
                    text='No se pudo abrir WhatsApp\nCrea el grupo manualmente',
                    text_size=(300, None),
                    halign='center'
                ),
                size_hint=(0.8, 0.4)
            )
            popup.open()

# Ejecutar la aplicación
if __name__ == '__main__':
    try:
        BiwengerApp().run()
    except Exception as e:
        print(f"Error al ejecutar la aplicación: {e}")
        import traceback
        traceback.print_exc()
