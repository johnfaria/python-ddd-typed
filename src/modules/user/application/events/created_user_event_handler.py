from typing import Any


from modules.user.domain.events.created_user_domain_event import CreatedUserDomainEvent


class CreatedUserDomainEventHandler:
    async def handle(self, event: CreatedUserDomainEvent) -> Any:
        raise NotImplementedError("Not implemented")
