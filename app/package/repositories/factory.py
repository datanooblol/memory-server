from ..data_models.user import User
from ..data_models.project import Project
from ..data_models.chat_session import ChatSession
from ..data_models.conversation import Conversation
from ..data_models.reference import Reference
from ..data_models.source import Source
from ..data_models.agent_execution import AgentExecution
from ..data_models.task import Task
from ..data_models.episode import Episode
from ..data_models.metadata import Metadata, FieldMetadata
from .generic_repository import GenericRepository
from .nosql_repository import NoSQLRepository

class RepositoryFactory:
    def __init__(self, storage):
        self.storage = storage
    
    def _get_repository(self, model_class, table_name, id_field):
        if hasattr(self.storage, 'put_item'):  # NoSQL storage
            return NoSQLRepository(self.storage, model_class, table_name, id_field)
        else:  # Relational storage
            return GenericRepository(self.storage, model_class, table_name, id_field)
    
    def get_user_repository(self):
        return self._get_repository(User, "users", "user_id")
    
    def get_project_repository(self):
        return self._get_repository(Project, "projects", "project_id")
    
    def get_chat_session_repository(self):
        return self._get_repository(ChatSession, "chat_sessions", "chat_session_id")
    
    def get_conversation_repository(self):
        return self._get_repository(Conversation, "conversations", "convo_id")
    
    def get_reference_repository(self):
        return self._get_repository(Reference, "references", "reference_id")
    
    def get_source_repository(self):
        return self._get_repository(Source, "sources", "source_id")
    
    def get_agent_execution_repository(self):
        return self._get_repository(AgentExecution, "agent_executions", "execution_id")
    
    def get_task_repository(self):
        return self._get_repository(Task, "tasks", "task_id")

    def get_episode_repository(self):
        return self._get_repository(Episode, "episodes", "episode_id")
    
    def get_metadata_repository(self):
        return self._get_repository(Metadata, "metadata", "metadata_id")
    
    def get_field_metadata_repository(self):
        return self._get_repository(FieldMetadata, "field_metadata", "field_id")