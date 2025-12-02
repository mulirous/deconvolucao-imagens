"""
Sistema de logging customizado para deconvolução.
"""

import logging
from typing import Optional, Callable
from datetime import datetime


class DeconvolutionLogger:
    """
    Logger customizado para algoritmos de deconvolução.
    Permite callbacks para atualização em tempo real na interface gráfica.
    """
    
    def __init__(self, callback: Optional[Callable[[str], None]] = None):
        """
        Inicializa o logger.
        
        Args:
            callback: Função opcional que será chamada para cada mensagem de log
        """
        self.callback = callback
        self.messages = []
    
    def info(self, message: str):
        """Registra uma mensagem de informação."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] INFO: {message}"
        self.messages.append(log_message)
        if self.callback:
            self.callback(log_message)
    
    def debug(self, message: str):
        """Registra uma mensagem de debug."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] DEBUG: {message}"
        self.messages.append(log_message)
        if self.callback:
            self.callback(log_message)
    
    def warning(self, message: str):
        """Registra uma mensagem de aviso."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] WARNING: {message}"
        self.messages.append(log_message)
        if self.callback:
            self.callback(log_message)
    
    def error(self, message: str):
        """Registra uma mensagem de erro."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] ERROR: {message}"
        self.messages.append(log_message)
        if self.callback:
            self.callback(log_message)
    
    def get_messages(self):
        """Retorna todas as mensagens de log."""
        return self.messages
    
    def clear(self):
        """Limpa todas as mensagens de log."""
        self.messages = []

