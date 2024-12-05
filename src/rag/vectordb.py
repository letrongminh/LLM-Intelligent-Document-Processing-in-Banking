from abc import ABC, abstractmethod
import logging

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams


logger = logging.getLogger(__name__)


class BaseVectorDatabase(ABC):
    @abstractmethod
    def create_collection(self, name: str, vector_size: int, distance_op: str):
        """
        Create a collection in Qdrant.
        Args:
            name: Name of the collection.
            vector_size: Dimension of the vectors (default: 1536).
            distance: Distance metric for similarity search (default: "DOT").
        """
        pass


    @abstractmethod
    def add_vectors(self, collection_name: str, vectors: dict):
        """
        Add vector list to a collection.
        Args:
            collection_name: Name of the collection.
            vectors: A dictionary where keys are vector IDs, and values contain vector data and payload.
        """
        pass

    @abstractmethod
    def search_vectors(self, collection_name: str, query_vector: list, limit: int):
        """
        Search for vectors in a collection.
        Args:
            collection_name: Name of the collection.
            query_vector: The vector to use for similarity search.
            limit: Number of results to return (default: 4).
        """
        pass


class QdrantDatabase(BaseVectorDatabase):
    def __init__(self, url: str):
        self.client = QdrantClient(url=url)
    
    def create_collection(self, name, vector_size, distance_op):
        return self.client.create_collection(
            collection_name=name,
            vectors_config=VectorParams(size=1536, distance=Distance.DOT)
        )
    
    def add_vectors(self, collection_name: str, vectors: dict):
        points = [
            PointStruct(id=k, vector=v["vector"], payload=v["payload"])
            for k, v in vectors.items()
        ]
        return self.client.upsert(collection_name=collection_name, points=points, wait=True)

    def search_vectors(self, collection_name: str, query_vector: list, limit: int = 4):
        results = self.client.search(
            collection_name=collection_name, query_vector=query_vector, limit=limit
        )
        return [x.payload for x in results]