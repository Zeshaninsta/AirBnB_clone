#!/usr/bin/python3
"""Defines class Review """

from models.base_model import BaseModel


class Review(BaseModel):
    """Class Review
       Public class attributes:
           place_id: string
           user_id: string
           text string
    """
    place_id = ""
    user_id = ""
    text = ""
