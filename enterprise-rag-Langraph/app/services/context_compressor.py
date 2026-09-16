import re
from typing import List
from app.core.logger import logger
import numpy as np
from sentence_transformers import SentenceTransformer

from app.schemas.retrieval import RetrievedChunk


class ContextCompressor:

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.40,
        max_tokens: int = 1000,
        preserve_neighbors: bool = True,
    ):
        """
        Context Compressor

        Pipeline:

        Reranked Chunks
                ↓
        Sentence Splitting
                ↓
        Sentence Embeddings
                ↓
        Query Embedding
                ↓
        Cosine Similarity
                ↓
        Relevant Sentence Selection
                ↓
        Neighbor Preservation
                ↓
        Token Budget
                ↓
        Compressed Chunks
        """

        # -----------------------------------------
        # Embedding model
        # -----------------------------------------

        self.model = SentenceTransformer(embedding_model)

        # -----------------------------------------
        # Configuration
        # -----------------------------------------

        self.similarity_threshold = similarity_threshold

        self.max_tokens = max_tokens

        self.preserve_neighbors = preserve_neighbors

    # =================================================
    # 1. Split text into sentences
    # =================================================

    def _split_sentences(self, text: str) -> List[str]:

        if not text or not text.strip():
            return []

        sentences = re.split(r"(?<=[.!?])\s+", text.strip())

        #         above make as below
        # sentences = [
        #     "Hello.",
        #     "How are you?",
        #     "I am fine."
        # ]

        return [sentence.strip() for sentence in sentences if sentence.strip()]

        # above is implementedd because ifresults might get like below
        # sentences = [

    #     "FastAPI is a framework.",
    #     "   ",
    #     "It is written in Python.",
    #     "",
    #     "   FastAPI is fast.   "
    # ]

    # =================================================
    # 2. Estimate tokens
    # =================================================

    def _estimate_tokens(self, text: str) -> int:
        """
        Approximate token calculation.

        Rough assumption:

            1 token ≈ 4 characters

        This is NOT an exact tokenizer.
        """

        if not text:
            return 0

        return max(1, len(text) // 4)

    # =================================================
    # 3. Select relevant sentences
    # =================================================

    def _select_relevant_sentences(self, query: str, sentences: List[str]) -> List[str]:

        if not sentences:
            return []

        # -----------------------------------------
        # Create query embedding
        # -----------------------------------------

        query_embedding = self.model.encode(query, normalize_embeddings=True)

        # -----------------------------------------
        # Create sentence embeddings
        # -----------------------------------------

        sentence_embeddings = self.model.encode(sentences, normalize_embeddings=True)

        # -----------------------------------------
        # Cosine similarity
        #
        # Since embeddings are normalized:
        #
        # cosine_similarity = dot_product
        # -----------------------------------------

        similarities = np.dot(sentence_embeddings, query_embedding)

        # -----------------------------------------
        # Find relevant sentences
        # -----------------------------------------

        relevant_indexes = []

        for index, similarity in enumerate(similarities):

            similarity = float(similarity)

            if similarity >= self.similarity_threshold:

                relevant_indexes.append(index)

        # -----------------------------------------
        # No relevant sentences
        # -----------------------------------------

        if not relevant_indexes:
            return []

        # -----------------------------------------
        # Preserve neighboring sentences
        # -----------------------------------------

        selected_indexes = set()

        for index in relevant_indexes:

            # Current sentence
            selected_indexes.add(index)

            if self.preserve_neighbors:

                # Previous sentence
                if index - 1 >= 0:

                    selected_indexes.add(index - 1)

                # Next sentence
                if index + 1 < len(sentences):

                    selected_indexes.add(index + 1)

        # -----------------------------------------
        # Keep original document order
        # -----------------------------------------

        selected_indexes = sorted(selected_indexes)

        # -----------------------------------------
        # Build final sentence list
        # -----------------------------------------

        selected_sentences = [sentences[index] for index in selected_indexes]

        return selected_sentences

    # =================================================
    # 4. Apply token limit
    # =================================================

    def _apply_token_limit(self, content: str, remaining_tokens: int) -> str:

        if not content:
            return ""

        if remaining_tokens <= 0:
            return ""

        content_tokens = self._estimate_tokens(content)

        # -----------------------------------------
        # Entire content fits
        # -----------------------------------------

        if content_tokens <= remaining_tokens:

            return content

        # -----------------------------------------
        # Need to truncate
        # -----------------------------------------

        max_characters = remaining_tokens * 4

        truncated_content = content[:max_characters]

        # -----------------------------------------
        # Avoid ending in the middle of a word
        # -----------------------------------------

        last_space = truncated_content.rfind(" ")

        if last_space > 0:

            truncated_content = truncated_content[:last_space]

        return truncated_content.strip()

    # =================================================
    # 5. Compress documents
    # =================================================

    def compress(
        self, query: str, documents: List[RetrievedChunk]
    ) -> List[RetrievedChunk]:
        try:
            logger.info("starting compress Service ")
            if not documents:
                return []

            compressed_documents = []

            current_tokens = 0

            # =================================================
            # Process reranked documents in order
            # =================================================

            for document in documents:

                # -----------------------------------------
                # Check global token budget
                # -----------------------------------------

                remaining_tokens = self.max_tokens - current_tokens

                if remaining_tokens <= 0:
                    break

                # -----------------------------------------
                # Split document into sentences
                # -----------------------------------------

                sentences = self._split_sentences(document.content)

                if not sentences:
                    continue

                # -----------------------------------------
                # Semantic sentence compression
                # -----------------------------------------

                relevant_sentences = self._select_relevant_sentences(
                    query=query, sentences=sentences
                )

                # -----------------------------------------
                # No relevant sentences
                # -----------------------------------------

                if not relevant_sentences:
                    continue

                # -----------------------------------------
                # Rebuild compressed document
                # -----------------------------------------

                compressed_content = " ".join(relevant_sentences)

                # -----------------------------------------
                # Apply token limit
                # -----------------------------------------

                compressed_content = self._apply_token_limit(
                    content=compressed_content, remaining_tokens=remaining_tokens
                )

                if not compressed_content:
                    break

                # -----------------------------------------
                # Calculate statistics
                # -----------------------------------------

                original_length = len(document.content)

                compressed_length = len(compressed_content)

                compression_ratio = compressed_length / max(1, original_length)

                original_tokens = self._estimate_tokens(document.content)

                compressed_tokens = self._estimate_tokens(compressed_content)

                # -----------------------------------------
                # Preserve original metadata
                # -----------------------------------------

                metadata = dict(document.meta_data)

                # -----------------------------------------
                # Add compression information
                # -----------------------------------------

                metadata["compression"] = {
                    "original_tokens": original_tokens,
                    "compressed_tokens": compressed_tokens,
                    "original_characters": original_length,
                    "compressed_characters": compressed_length,
                    "compression_ratio": round(compression_ratio, 3),
                    "similarity_threshold": self.similarity_threshold,
                    "preserve_neighbors": self.preserve_neighbors,
                }

                # -----------------------------------------
                # Create compressed RetrievedChunk
                # -----------------------------------------

                compressed_document = RetrievedChunk(
                    chunk_id=document.chunk_id,
                    content=compressed_content,
                    score=document.retrieval_score,
                    metadata=metadata,
                )

                compressed_documents.append(compressed_document)

                # -----------------------------------------
                # Update global token count
                # -----------------------------------------

                current_tokens += compressed_tokens

            return compressed_documents
        except Exception as error:
            raise error
