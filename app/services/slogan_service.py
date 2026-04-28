from app.extensions import SessionLocal
from app.models.slogan_request import SloganRequest
from app.models.slogan import Slogan
from app.services.llm_service import generate_from_llm
from app.utils.parser import parse_llm_response


def create_slogans(entity_name: str, description: str, core_values: str, language: str, total: int):
    """Generate slogan/tagline menggunakan LLM dan simpan ke database."""
    session = SessionLocal()
    try:
        # Tentukan instruksi bahasa
        if language == "en":
            lang_instruction = "in English only"
            lang_label = "en"
        elif language == "both":
            lang_instruction = "in both Bahasa Indonesia and English (alternating)"
            lang_label = "both"
        else:
            lang_instruction = "in Bahasa Indonesia only"
            lang_label = "id"

        prompt = f"""
        Dalam format JSON, buat {total} slogan atau tagline kreatif untuk entitas berikut:
        - Nama Entitas: {entity_name}
        - Deskripsi Singkat: {description}
        - Nilai Utama: {core_values}
        - Bahasa: {lang_instruction}

        Format respons HARUS persis seperti ini (JSON saja, tanpa teks lain):
        {{
            "slogans": [
                {{"text": "...", "language": "id"}},
                {{"text": "...", "language": "en"}}
            ]
        }}

        Pastikan setiap slogan singkat, berkesan, dan mencerminkan nilai utama entitas.
        Jika bahasa "both", buat selang-seling Bahasa Indonesia dan Inggris.
        Jika bahasa "id", gunakan field language = "id" untuk semua.
        Jika bahasa "en", gunakan field language = "en" untuk semua.
        """

        result = generate_from_llm(prompt)
        slogans = parse_llm_response(result)

        # Simpan request log
        req_log = SloganRequest(
            entity_name=entity_name,
            description=description,
            core_values=core_values,
            language=lang_label,
        )
        session.add(req_log)
        session.commit()

        # Simpan setiap slogan
        saved = []
        for item in slogans:
            text = item.get("text", "")
            lang = item.get("language", lang_label)
            if text:
                s = Slogan(text=text, language=lang, request_id=req_log.id)
                session.add(s)
                saved.append({"text": text, "language": lang})

        session.commit()
        return saved

    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_all_slogans(page: int = 1, per_page: int = 100):
    """Ambil semua slogan dari database dengan paginasi."""
    session = SessionLocal()
    try:
        query = session.query(Slogan)
        total = query.count()
        data = (
            query
            .order_by(Slogan.id.desc())
            .offset((page - 1) * per_page)
            .limit(per_page)
            .all()
        )
        result = [
            {
                "id": s.id,
                "text": s.text,
                "language": s.language,
                "request_id": s.request_id,
                "created_at": s.created_at.isoformat(),
            }
            for s in data
        ]
        return {
            "page": page,
            "per_page": per_page,
            "total": total,
            "total_pages": (total + per_page - 1) // per_page if total > 0 else 0,
            "data": result,
        }
    finally:
        session.close()


def get_slogan_by_id(slogan_id: int):
    """Ambil detail satu slogan beserta metadata request-nya."""
    session = SessionLocal()
    try:
        slogan = session.query(Slogan).filter(Slogan.id == slogan_id).first()
        if not slogan:
            return None

        req = session.query(SloganRequest).filter(SloganRequest.id == slogan.request_id).first()

        return {
            "id": slogan.id,
            "text": slogan.text,
            "language": slogan.language,
            "request_id": slogan.request_id,
            "created_at": slogan.created_at.isoformat(),
            "request": {
                "id": req.id,
                "entity_name": req.entity_name,
                "description": req.description,
                "core_values": req.core_values,
                "language": req.language,
                "created_at": req.created_at.isoformat(),
            } if req else None,
        }
    finally:
        session.close()
