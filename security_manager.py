#!/usr/bin/env python3
"""
🔐 Security Manager - Sistema de seguridad para el bot
Gestiona usuarios, roles y permisos
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Paths
BASE_DIR = Path(__file__).parent
SECURITY_FILE = BASE_DIR / "security.json"
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)


class SecurityManager:
    """Gestiona seguridad y permisos del bot"""
    
    # Niveles de acceso
    ROLES = {
        "owner": 100,      # Acceso total
        "admin": 50,       # Acceso a comandos admin
        "premium": 20,     # Acceso a comandos premium
        "user": 10,        # Acceso básico
        "banned": 0        # Sin acceso
    }
    
    # Comandos por nivel de acceso
    COMMAND_PERMISSIONS = {
        # Nivel 0 - Públicos (todos pueden usar)
        "start": 10,
        "help": 10,
        "ayuda": 10,
        
        # Nivel 10 - Usuarios registrados
        "generar": 10,
        "prompts": 10,
        "noticias": 10,
        "stats": 10,
        "ia": 10,
        
        # Nivel 20 - Premium
        "campana": 20,
        "post": 20,
        "imagen": 20,
        
        # Nivel 50 - Admins
        "admin": 50,
        "setup": 50,
        "setgnews": 50,
        "sethf": 50,
        "setpexels": 50,
        "broadcast": 50,
        "users": 50,
        
        # Nivel 100 - Owner
        "grant": 100,
        "revoke": 100,
        "ban": 100,
        "unban": 100,
        "security": 100,
    }
    
    def __init__(self):
        self.security_data = self.load_security()
    
    def load_security(self) -> dict:
        """Cargar datos de seguridad"""
        default_data = {
            "owner_id": None,
            "admins": [],
            "premium_users": [],
            "banned_users": [],
            "allowed_groups": [],
            "require_approval": False,
            "pending_approvals": [],
            "access_log": []
        }
        
        if SECURITY_FILE.exists():
            with open(SECURITY_FILE, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
                # Merge con defaults
                for key in default_data:
                    if key not in saved_data:
                        default_data[key] = saved_data.get(key, default_data[key])
        
        return default_data
    
    def save_security(self):
        """Guardar datos de seguridad"""
        with open(SECURITY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.security_data, f, indent=2, ensure_ascii=False)
    
    def set_owner(self, user_id: int):
        """Establecer owner del bot"""
        self.security_data["owner_id"] = user_id
        self.save_security()
    
    def get_owner(self) -> Optional[int]:
        """Obtener ID del owner"""
        return self.security_data.get("owner_id")
    
    def add_admin(self, user_id: int):
        """Añadir admin"""
        if user_id not in self.security_data["admins"]:
            self.security_data["admins"].append(user_id)
            self.save_security()
    
    def remove_admin(self, user_id: int):
        """Remover admin"""
        if user_id in self.security_data["admins"]:
            self.security_data["admins"].remove(user_id)
            self.save_security()
    
    def add_premium(self, user_id: int):
        """Añadir usuario premium"""
        if user_id not in self.security_data["premium_users"]:
            self.security_data["premium_users"].append(user_id)
            self.save_security()
    
    def remove_premium(self, user_id: int):
        """Remover premium"""
        if user_id in self.security_data["premium_users"]:
            self.security_data["premium_users"].remove(user_id)
            self.save_security()
    
    def ban_user(self, user_id: int):
        """Banear usuario"""
        if user_id not in self.security_data["banned_users"]:
            self.security_data["banned_users"].append(user_id)
            self.save_security()
    
    def unban_user(self, user_id: int):
        """Desbanear usuario"""
        if user_id in self.security_data["banned_users"]:
            self.security_data["banned_users"].remove(user_id)
            self.save_security()
    
    def allow_group(self, group_id: int):
        """Permitir grupo"""
        if group_id not in self.security_data["allowed_groups"]:
            self.security_data["allowed_groups"].append(group_id)
            self.save_security()
    
    def remove_group(self, group_id: int):
        """Remover grupo permitido"""
        if group_id in self.security_data["allowed_groups"]:
            self.security_data["allowed_groups"].remove(group_id)
            self.save_security()
    
    def get_user_role(self, user_id: int) -> str:
        """Obtener rol del usuario"""
        if user_id == self.security_data.get("owner_id"):
            return "owner"
        elif user_id in self.security_data["admins"]:
            return "admin"
        elif user_id in self.security_data["premium_users"]:
            return "premium"
        elif user_id in self.security_data["banned_users"]:
            return "banned"
        else:
            return "user"
    
    def get_user_level(self, user_id: int) -> int:
        """Obtener nivel de acceso del usuario"""
        role = self.get_user_role(user_id)
        return self.ROLES.get(role, 10)
    
    def can_use_command(self, user_id: int, command: str) -> bool:
        """Verificar si el usuario puede usar un comando"""
        # Owner tiene acceso total
        if user_id == self.security_data.get("owner_id"):
            return True
        
        # Verificar si está baneado
        if user_id in self.security_data["banned_users"]:
            return False
        
        # Obtener nivel requerido para el comando
        required_level = self.COMMAND_PERMISSIONS.get(command, 10)
        
        # Obtener nivel del usuario
        user_level = self.get_user_level(user_id)
        
        # Verificar si tiene nivel suficiente
        return user_level >= required_level
    
    def log_access(self, user_id: int, username: str, command: str, allowed: bool):
        """Registrar acceso en log"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "username": username,
            "command": command,
            "allowed": allowed
        }
        
        self.security_data["access_log"].append(log_entry)
        
        # Mantener solo últimos 1000 registros
        if len(self.security_data["access_log"]) > 1000:
            self.security_data["access_log"] = self.security_data["access_log"][-1000:]
        
        self.save_security()
    
    def get_access_log(self, limit: int = 50) -> List[dict]:
        """Obtener log de accesos"""
        return self.security_data["access_log"][-limit:]
    
    def get_all_users(self) -> dict:
        """Obtener todos los usuarios con sus roles"""
        return {
            "owner": self.security_data.get("owner_id"),
            "admins": self.security_data["admins"],
            "premium": self.security_data["premium_users"],
            "banned": self.security_data["banned_users"]
        }
    
    def get_stats(self) -> dict:
        """Obtener estadísticas de seguridad"""
        return {
            "owner_count": 1 if self.security_data.get("owner_id") else 0,
            "admin_count": len(self.security_data["admins"]),
            "premium_count": len(self.security_data["premium_users"]),
            "banned_count": len(self.security_data["banned_users"]),
            "group_count": len(self.security_data["allowed_groups"]),
            "log_entries": len(self.security_data["access_log"])
        }


# Instancia global
security = SecurityManager()


def check_permission(user_id: int, command: str) -> bool:
    """Función helper para verificar permisos"""
    return security.can_use_command(user_id, command)


def get_role_name(user_id: int) -> str:
    """Obtener nombre del rol"""
    return security.get_user_role(user_id)
