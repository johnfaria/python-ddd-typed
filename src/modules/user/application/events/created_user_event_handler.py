from modules.user.domain.events.created_user_domain_event import CreatedUserDomainEvent


class CreatedUserDomainEventHandler:
    async def handle(self, event: CreatedUserDomainEvent):
        raise NotImplementedError("Not implemented")
