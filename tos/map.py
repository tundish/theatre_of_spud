#!/usr/bin/env python3
# encoding: utf-8

# This is a parser-based, web-enabled narrative.
# Copyright (C) 2021 D E Haynes

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import enum

from tos.types import Navigator


class Map(Navigator):

    spots = {
        "auditorium": ["auditorium"],
        "backstage": ["backstage"],
        "balcony": ["balcony", "downstairs"],
        "bar": ["bar"],
        "car_park": ["car park"],
        "cloaks": ["cloakroom", "cloaks"],
        "corridor": ["corridor"],
        "costume": ["costume store", "props room"],
        "foyer": ["foyer"],
        "kitchen": ["kitchen"],
        "lighting": ["lighting box"],
        "office": ["box office", "office"],
        "passage": ["passage"],
        "stage": ["stage", "onstage"],
        "stairs": ["stairs", "upstairs"],
        "wings": ["wings", "stage left", "stage right"],
    }

    Arriving = enum.Enum("Arriving", spots, type=Navigator)
    Departed = enum.Enum("Departed", spots, type=Navigator)
    Location = enum.Enum("Location", spots, type=Navigator)

    def __init__(self):
        self.topology = {
            "auditorium": ["balcony", "corridor", "passage"],
            "backstage": ["costume", "wings"],
            "balcony": ["auditorium", "bar"],
            "bar": ["foyer", "kitchen", "stairs", "passage"],
            "car_park": ["foyer"],
            "cloaks": ["foyer"],
            "corridor": ["auditorium", "foyer", "wings"],
            "costume": ["backstage", "wings"],
            "foyer": ["car_park", "corridor", "office", "cloaks", "bar"],
            "kitchen": ["bar"],
            "lighting": ["balcony", "stairs"],
            "office": ["foyer"],
            "passage": ["auditorium", "bar", "wings"],
            "stage": ["wings"],
            "stairs": ["auditorium", "balcony", "bar", "lighting"],
            "wings": ["backstage", "corridor", "costume", "passage", "stage"],
        }

        self.scenery = {
            "auditorium": [
            ],
            "backstage": [
            ],
            "balcony": [
            ],
            "bar": [
            ],
            "car_park": [
                "a Car Park in front of the Theatre", "the Car Park belonging to the Theatre",
                "front of the Theatre"
            ],
            "cloaks": [
            ],
            "corridor": [
            ],
            "costume": [
            ],
            "foyer": [
            ],
            "kitchen": [
            ],
            "lighting": [
            ],
            "office": [
            ],
            "passage": [
            ],
            "stage": [
            ],
            "stairs": [
            ],
            "wings": [
            ],
        }

# Required for pickling

Arriving = Map.Arriving
Departed = Map.Departed
Location = Map.Location
