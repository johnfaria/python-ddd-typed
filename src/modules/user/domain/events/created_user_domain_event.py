from core.domain.protocols.domain_event_protocol import DomainEvent
from dataclasses import dataclass


@dataclass(frozen=True)
class CreatedUserDomainEvent(DomainEvent): ...
