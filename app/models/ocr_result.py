import uuid

from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class OcrResult(Base, TimestampMixin):
    __tablename__ = "ocr_results"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    factura_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("facturas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Raw output from the recognition stage (all lines joined by \n)
    raw_text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Heuristically extracted fields
    extracted_date: Mapped[str | None] = mapped_column(String(50), nullable=True)
    extracted_total: Mapped[str | None] = mapped_column(String(50), nullable=True)
    extracted_provider: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Rough confidence score in [0, 1] based on how many fields were found
    confidence_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)

    # Human-readable notes produced by the pipeline (comma-separated)
    processing_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Pipeline status: processing | processed | needs_review | failed
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="processing")

    factura: Mapped["Factura"] = relationship("Factura", back_populates="ocr_results")  # type: ignore[name-defined]
