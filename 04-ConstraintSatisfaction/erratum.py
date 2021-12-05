#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    This file implements functionality to print errors, debug messages,
    and specific info in a distinct way to separate it from normal output.
    
"""
__author__ = "Amittai"
__copyright__ = "Copyright 2021"
__credits__ = ["Amittai"]
__email__ = "Amittai.J.Wekesa.24@dartmouth.edu"
__github__ = "@siavava"

#### exports: log_error, log_info, log_debug_info ####


def __text_color(r: int, g: int, b: int, text: str):
    """
        This function is used to generate colored text in the terminal.
        Used internally and not intended to be called directly.
    """
    return f"\033[1m\033[38;2;{r};{g};{b}m{text} \033[38;2;255;255;255m\033[0m"


def log_error(*args):
    """
        Given a list of arguments presumably representing an error message,
        this function prints them in a distinct way to separate them from normal output.
    """
    err_message = ""
    for arg in args:
        err_message += str(arg) + " "
        
    print(__text_color(220, 20, 60, err_message))
    
def log_info(*args):
    """
        Given a list of arguments presumably representing useful information,
        this function prints them in a distinct way to separate them from normal output.
    """
    err_message = ""
    for arg in args:
        err_message += str(arg) + " "
        
    print(__text_color(30, 144, 255, err_message))
    
def log_debug_info(*args):
    """
        Given a list of arguments presumably representing debug information,
        this function prints them in a distinct way to separate them from normal output.
    """
    debug_message = ""
    for arg in args:
        debug_message += str(arg) + " "
        
    print(__text_color(55, 155, 55, debug_message))
    
    
if __name__ == "__main__":
    log_error("Hello", "World")
    log_info("Hello", "World")
    log_debug_info("Hello", "World")