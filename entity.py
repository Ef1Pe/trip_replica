"""Entity definition that ties metadata and server together."""

from dataclasses import dataclass
from typing import Optional

from metadata import TripReplicaMetadata
from server import start_server


@dataclass
class TripReplicaEntity:
  """Simple facade for launching the replica webserver."""

  port: int = 5000
  metadata: TripReplicaMetadata = TripReplicaMetadata()

  def run(self, content: Optional[dict] = None) -> None:
    if content:
      # Inject provided content before starting server
      from server import injected_content

      injected_content.append(content)
    start_server(self.port)


if __name__ == "__main__":
  TripReplicaEntity().run()
