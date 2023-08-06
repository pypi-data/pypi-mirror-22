#!/usr/bin/env python3

       ###############
      # SKYCHAT API #
     # IN PYTHON   #
    ###############

import requests
import json
from socketIO_client import SocketIO, LoggingNamespace
from socketIO_client.exceptions import *
import re

class Room:
    def __init__(self, room_dict={}):
        self.name       = room_dict.get("name", False)
        self.picture    = room_dict.get("picture", False)
        self.background = room_dict.get("background", False)

class SkyChatClient:
    SERVER_ADDRESS = 'redsky.fr'
    SERVER_PORT    = 8056

    def __init__(self, pseudo=None, password=None, room=0, roompwd=None, refresh=10):
        """ Standard client for the SkyChat 2.0

        pseudo   -- account name
        password -- password (why do I even document that ?)
            | If pseudo & password are empty, you will login as a dirty Hamster
        room     -- Number of the room where you want yur bot to be
        roompwd  -- Room password, if room is locked
        refresh  -- duration of the each SocketIO.wait()
        """
        self.pseudo      = pseudo
        self.password    = password # I know, I shouldn't save it raw so #TODO fix it
        self.credentials = None
        self.room        = int(room)
        self.roompwd     = roompwd
        self.logged      = False
        self._refresh    = refresh
        self.room_info   = Room()

        self._init_socket()

        self.on_creation()

    def _init_socket(self):
        """ Creates and initiate socket """
        # Create socket
        self.sock = SocketIO(self.SERVER_ADDRESS, self.SERVER_PORT, LoggingNamespace, wait_for_connection=False)

        # Connection/Disconnection
        self.sock.on('connect',    self._connect_handler)
        self.sock.on('disconnect', self.on_disconnect)
        self.sock.on('reconnect',  self._reconnect_handler)

        # All types of messages
        self.sock.on('message',        self._message_handler)
        self.sock.on('connected_list', self.on_connected_list)
        self.sock.on('typing_list',    self.on_typing_list)
        self.sock.on('pseudo_info',    self._pseudo_info_handler)
        self.sock.on('room_update',    self.on_room_update)
        self.sock.on('mouse_position', self.on_mouse_position)
        self.sock.on('room_info',      self._room_info_handler)
        self.sock.on('kick',           self.on_kick)

    def _get_login_token(self, pseudo, password):
        """ Sends login info to get the token... All the info are stored in
        self.credentials """
        self.credentials = json.loads(requests.post("http://redsky.fr/ajax/account/api2.php", {'pseudo' : pseudo, 'pass' : password}).text)

    def _log_in(self):
        """ Called when the client has joined the server, and must now send its
        credentials and log in a room
        """
        # Get credentials
        if self.password:
            self._get_login_token(self.pseudo, self.password)

        # Login
        self.sock.emit('log', self.credentials)
        self.msgsend('/join %d%s' % (self.room, (' ' + self.roompwd if self.roompwd else '')))

        if not self.credentials:
            if self.pseudo:
                self.msgsend("/nick %s" % (self.pseudo))
            self.on_login()

    def msgsend(self, msg):
        """ Sends a standard message in the current room

        msg -- text to send
        """
        self.sock.emit('message', {'message' : msg})

    def pmsend(self, target, msg):
        """ Sends a private message to a user

        target -- target user name (not case sensitive)
        msg    -- text to send
        """
        self.msgsend("/mp %s %s" % (target, msg))

    def set_typing(self, state):
        """ Indicates to the server that you started or stopped typing

        state -- boolean, indicates whether you start or stop
        """
        self.sock.emit('typing', {'currently_typing' : state})

    def upload_file(self, filepath):
        """ Tries to upload a file on redsky.fr server, in order to be able to
        display it on the chat

        filepath -- path to file on the users local filesystem

        Returns the file url if the upload succeeded, None otherwise (error
        handling is still quite rough at this url)
        """
        ans = requests.post(
            "http://redsky.fr/ajax/fun/chat/img.php?&minimal=&notext=",
            files={'fichier' : open(filepath, 'rb')},
            data={"testval" : 1, "imgid" : "", "inputid" : "skychat_form_message_input"})
        try:
            return(re.findall("\"(http://redsky.fr/picts/galerie/uploaded/[^\"]*)\"", ans.text)[0])
        except IndexError:
            return(None)

      ###########################
     # PRIVATE EVENTS HANDLERS #
    ###########################

    def _message_handler(self, msg):
        """ Pre-treats messages, before passing it to self.on_message

        msg -- the received message, in form of a dict (if it is of another
               type, it will be refused
        """
        if type(msg) != dict:
            return
        if 'old' in msg:
            self.on_old_message(msg)
        elif msg['message_type'] == 'user_mp':
            self.on_private_message(msg)
        else:
            self.on_message(msg)

    def _pseudo_info_handler(self, msg):
        if msg['logged'] and self.credentials and not self.logged:
            self.on_login()
            self.logged = True
        self.on_pseudo_info(msg)

    def _connect_handler(self):
        self._log_in()
        self.on_connect()

    def _reconnect_handler(self):
        self._log_in()
        self.on_reconnect()

    def _room_info_handler(self, msg):
        self.room_info = Room(msg)
        self.on_room_info(msg)

      ###################
     # PUBLIC HANDLERS #
    ###################

    def on_connect(self):
        """ Called when the socket connects to the server
        Can be overridden """
        pass

    def on_disconnect(self):
        """ Called when the socket is disconnected from the server
        Can be overridden """
        pass

    def on_reconnect(self):
        """ Called when the socket reconnects after a disconnection from the
        server
        Can be overridden """
        pass

    def on_creation(self):
        """ Called when the client is created
        Useful to add elements to __init__
        Can be overridden """
        pass

    def on_login(self):
        """ Called when the client connects
        Can be overridden """
        pass

    def on_message(self, msg):
        """ Called when a message is received
        Can be overridden """
        pass

    def on_private_message(self, msg):
        """ Called when a private message is received
        Can be overridden """
        pass

    def on_old_message(self, msg):
        """ Called when old messages are loaded, at the connection
        Can be overridden """
        pass

    def on_pseudo_info(self, msg):
        """ Called when the server gives new infos about the pseudo
        Can be overridden """
        pass

    def on_room_update(self, msg):
        """ Called when something changes in the room
        Can be overridden  """
        pass

    def on_connected_list(self, msg):
        """ Called when the connected list is update, when somebody joined or
        leaved
        Can be overridden """
        pass

    def on_typing_list(self, msg):
        """ Called when the typing list is updated
        Can be overridden """
        pass

    def on_mouse_position(self, msg):
        """ Called when someone's mouse curser moves
        Totally useless, I know...
        But quite cool right ?
        Can be overridden """
        pass

    def on_room_info(self, msg):
        """ Called when some infos about the current room change, like its
        name or background
        Can be overridden """
        pass

    def on_kick(self, msg):
        """ Called when the client has been kicked; useful to auto-reconnect
        a bot, for instance
        Can be overridden """
        pass

    def run(self):
        while True:
            try:
                self.sock.wait(self._refresh)
            except (ConnectionError, IndexError):
                pass
