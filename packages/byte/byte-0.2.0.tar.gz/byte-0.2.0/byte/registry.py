# -*- coding: utf-8 -*-

"""Contains the class registry structures."""

from __future__ import absolute_import, division, print_function


class Registry(object):
    """Class registry structure."""

    models = set()

    @classmethod
    def register_model(cls, model):
        """
        Register data model.

        :param model: Data model
        :type model: class
        """
        cls.models.add(model)
