import uuid

from supabase import AsyncClient, acreate_client

from app.core.config import settings

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}

_client: AsyncClient | None = None


async def _get_client() -> AsyncClient:
    global _client
    if _client is None:
        _client = await acreate_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return _client


def validate_image(filename: str, content_type: str, size_bytes: int) -> None:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS or content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(
            f"Tipo de archivo no permitido. Se aceptan: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if size_bytes > max_bytes:
        raise ValueError(
            f"El archivo supera el tamanio maximo de {settings.MAX_UPLOAD_SIZE_MB} MB"
        )


async def upload_image(file_bytes: bytes, original_filename: str, content_type: str) -> str:
    ext = original_filename.rsplit(".", 1)[-1].lower()
    storage_path = f"{uuid.uuid4()}.{ext}"

    client = await _get_client()

    try:
        await client.storage.from_(settings.SUPABASE_BUCKET).upload(
            path=storage_path,
            file=file_bytes,
            file_options={"content-type": content_type, "upsert": "false"},
        )
    except Exception as exc:
        raise RuntimeError(f"Error al subir imagen a Supabase Storage: {exc}") from exc

    public_url: str = client.storage.from_(settings.SUPABASE_BUCKET).get_public_url(storage_path)
    return public_url
