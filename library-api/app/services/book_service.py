from datetime import date
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.book import BookModel
from app.schemas.book import BookCreate, BookUpdate, BookResponse, BookFilter


class BookService:
    """Serviço para operações de negócio relacionadas a livros."""

    def __init__(self, db: Session):
        """Inicializa o serviço com uma sessão do banco de dados.
        
        Args:
            db: Sessão do SQLAlchemy
        """
        self.db = db

    def create(self, book_data: BookCreate) -> BookResponse:
        """Cria um novo livro no banco de dados.
        
        Args:
            book_data: Dados do livro a ser criado
            
        Returns:
            BookResponse: Livro criado com ID gerado
        """
        book = BookModel(
            title=book_data.title,
            author=book_data.author,
            publication_date=book_data.publication_date,
            summary=book_data.summary
        )
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return BookResponse.model_validate(book)

    def get_all(self, filters: Optional[BookFilter] = None) -> List[BookResponse]:
        """Lista todos os livros com filtros opcionais.
        
        Args:
            filters: Filtros opcionais por título e/ou autor (case-insensitive, partial match)
            
        Returns:
            List[BookResponse]: Lista de livros filtrados
        """
        query = select(BookModel)
        
        if filters:
            if filters.title:
                query = query.where(BookModel.title.ilike(f"%{filters.title}%"))
            if filters.author:
                query = query.where(BookModel.author.ilike(f"%{filters.author}%"))
        
        result = self.db.execute(query)
        books = result.scalars().all()
        return [BookResponse.model_validate(b) for b in books]

    def get_by_id(self, book_id: int) -> Optional[BookResponse]:
        """Busca um livro pelo ID.
        
        Args:
            book_id: ID do livro a ser buscado
            
        Returns:
            BookResponse se encontrado, None caso contrário
        """
        result = self.db.execute(select(BookModel).where(BookModel.id == book_id))
        book = result.scalar_one_or_none()
        return BookResponse.model_validate(book) if book else None

    def update(self, book_id: int, book_data: BookUpdate) -> Optional[BookResponse]:
        """Atualiza um livro existente.
        
        Args:
            book_id: ID do livro a ser atualizado
            book_data: Dados parciais para atualização (campos não enviados são ignorados)
            
        Returns:
            BookResponse atualizado se encontrado, None caso contrário
        """
        result = self.db.execute(select(BookModel).where(BookModel.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return None
        
        update_data = book_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(book, field, value)
        
        self.db.commit()
        self.db.refresh(book)
        return BookResponse.model_validate(book)

    def delete(self, book_id: int) -> bool:
        """Remove um livro do banco de dados.
        
        Args:
            book_id: ID do livro a ser removido
            
        Returns:
            True se removido com sucesso, False se não encontrado
        """
        result = self.db.execute(select(BookModel).where(BookModel.id == book_id))
        book = result.scalar_one_or_none()
        if not book:
            return False
        self.db.delete(book)
        self.db.commit()
        return True
