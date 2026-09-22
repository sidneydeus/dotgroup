from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.book import BookCreate, BookResponse, BookFilter
from app.services.book_service import BookService

router = APIRouter(prefix="/books", tags=["books"])


def get_book_service(db: Session = Depends(get_db)) -> BookService:
    """Dependency injection para obter instância do BookService com sessão do banco."""
    return BookService(db)


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreate, service: BookService = Depends(get_book_service)):
    """
    Cria um novo livro no sistema.
    
    Args:
        book: Dados do livro a ser criado (title, author, publication_date, summary)
        service: Instância do BookService injetada via dependency injection
    
    Returns:
        BookResponse: Livro criado com ID gerado
    """
    return service.create(book)


@router.get("/", response_model=list[BookResponse])
def list_books(
    title: Optional[str] = Query(None, description="Filter by title (partial match)"),
    author: Optional[str] = Query(None, description="Filter by author (partial match)"),
    service: BookService = Depends(get_book_service)
):
    """
    Lista livros com filtros opcionais por título e/ou autor.
    
    Args:
        title: Filtro parcial por título (case-insensitive)
        author: Filtro parcial por autor (case-insensitive)
        service: Instância do BookService injetada via dependency injection
    
    Returns:
        list[BookResponse]: Lista de livros filtrados
    """
    filters = BookFilter(title=title, author=author)
    return service.get_all(filters)
