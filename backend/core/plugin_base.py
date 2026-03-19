from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Type
from fastapi import APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel


class CardField(BaseModel):
    """Defines a field in the card layout."""
    key: str
    label: str
    type: str = "text"  # text, date, link, badge, list, tags
    icon: Optional[str] = None
    class_name: Optional[str] = None


class CardLayout(BaseModel):
    """Defines how cards should be rendered for this plugin."""
    title_field: str
    title_link_field: Optional[str] = None  # Field containing URL for title link
    subtitle_fields: List[CardField] = []
    body_fields: List[CardField] = []
    badge_field: Optional[CardField] = None
    icon: str = "Box"
    color: str = "gray"


class PluginConfig(BaseModel):
    """Configuration for a plugin."""
    name: str
    enabled: bool = True
    display_name: str
    description: str = ""
    icon: str = "Box"
    color: str = "gray"
    order: int = 0
    settings: Dict[str, Any] = {}


class BasePlugin(ABC):
    """Base class for all plugins."""
    
    name: str = "base"
    display_name: str = "Base Plugin"
    description: str = ""
    version: str = "1.0.0"
    
    def __init__(self, config: Optional[PluginConfig] = None):
        self.config = config or PluginConfig(
            name=self.name,
            display_name=self.display_name,
            description=self.description
        )
        self._router: Optional[APIRouter] = None
    
    @abstractmethod
    def get_models(self) -> List[Type]:
        """Return SQLAlchemy model classes for this plugin."""
        pass
    
    @abstractmethod
    def get_router(self) -> APIRouter:
        """Return FastAPI router with all routes for this plugin."""
        pass
    
    @abstractmethod
    def get_card_layout(self) -> CardLayout:
        """Return the card layout configuration for the frontend."""
        pass
    
    @abstractmethod
    def get_dashboard_query(self, db: Session, limit: int = 3) -> Dict[str, Any]:
        """Return dashboard data with items and total count."""
        pass
    
    def on_load(self):
        """Called when plugin is loaded."""
        pass
    
    def on_unload(self):
        """Called when plugin is unloaded."""
        pass
    
    def on_config_change(self, new_config: PluginConfig):
        """Called when plugin configuration changes."""
        self.config = new_config


class PluginMetadata(BaseModel):
    """Metadata about a loaded plugin."""
    name: str
    display_name: str
    description: str
    version: str
    enabled: bool
    icon: str
    color: str
    order: int
    route_prefix: str
    card_layout: CardLayout
