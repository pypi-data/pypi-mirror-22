#!/usr/bin/env python2
# -*- coding: utf8 -*-

import re

from taemin import schema
from taemin import plugin

from .save_schema import Savedthings

class TaeminSave(plugin.TaeminPlugin):
    helper = {"save": "Sauvegarde du contenu. Usage: !save lien/texte or !save quote user number or !save send"}

    def on_pubmsg(self, msg):
        if msg.key != "save":
            return

        chan = msg.chan.name

        if msg.value == "":
            self.privmsg(chan, "Veuillez préciser le contenu à sauvegarder")
            return

        kws = re.search(r'quote\s+(\w+)\s+(\d+)', msg.value)
        if kws is None:
            self.saveothers(msg, chan)
            return

        quoteduser = self.get_user(kws.group(1), chan)
        quotedmsg = self.get_message(quoteduser, msg.chan, int(kws.group(2)))

        Savedthings.create(user=msg.user, content=quotedmsg.message)

        self.privmsg(chan, "Le contenu a bien été sauvegardé")

    def saveothers(self, msg, chan):
        subj = re.search(r'send\s*(.+)?', msg.value)
        if subj is None:
            self.savecontent(msg)
        else:
            sauvegarde = Savedthings.select().where(Savedthings.user == msg.user)
            tablesauvegarde = self.parsecontent(sauvegarde)
            if subj.group(1) is None:
                self.taemin.mailation.mailage(msg.chan.name, tablesauvegarde, msg.user, "Sauvegarde IRC")
            else:
                self.privmsg(chan, subj.group(1))
                self.taemin.mailation.mailage(msg.chan.name, tablesauvegarde, msg.user, subj.group(1))
            suppr = Savedthings.delete().where(Savedthings.user == msg.user)
            suppr.execute()


    def savecontent(self, msg):
        Savedthings.create(user=msg.user, content=msg.value)

    def parsecontent(self, sauvegarde):
        tableau = []
        for line in sauvegarde:
            tableau.append(line.content)
        return tableau


    def get_message(self, user, chan, limit=1):
        quotes = [quote for quote in schema.Message
                  .select()
                  .where((schema.Message.user == user) & (schema.Message.chan == chan))
                  .order_by(schema.Message.created_at.desc())
                  .offset(limit - 1).limit(1)]

        if not quotes:
            return None

        return quotes[0]

    def get_user(self, name, chan):
        try:
            return schema.User.get(schema.User.name % name)
        except schema.User.DoesNotExist:
            self.privmsg(chan, "L'utilisateur n'est pas enregistré")
            return None
