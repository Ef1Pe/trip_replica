"""Metadata schema for Trip.com replica entity."""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Metadata:
  domain: str
  parameters: Dict[str, str] = field(default_factory=dict)


class TripReplicaMetadata:
  """Defines injectable parameters for dynamic content."""

  def get_metadata(self) -> Metadata:
    return Metadata(
      domain="*.trip.com",
      parameters={
        "section": "string",
        "target": "string",
        "component": "string",
        "title": "string",
        "subtitle": "string",
        "image": "string",
        "badge": "string",
        "tag": "string",
        "cta": "string",
      },
    )


metadata_schema = TripReplicaMetadata().get_metadata()
