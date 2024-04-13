from dependency_inspector import containers, providers

from .charity_project import ChatityProjectRepository


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    charity_project_repository = providers.Factory(
        ChatityProjectRepository, session=config.db.session
    )
