from flask import Blueprint, request, jsonify
from app.services.slogan_service import create_slogans, get_all_slogans, get_slogan_by_id

slogan_bp = Blueprint("slogan", __name__)


@slogan_bp.route("/slogans/generate", methods=["POST"])
def generate():
    """
    POST /slogans/generate
    Body JSON:
      - entity_name  (str, wajib)  : nama produk/komunitas/kampanye
      - description  (str, wajib)  : deskripsi singkat
      - core_values  (str, wajib)  : nilai utama (bisa koma-separated)
      - total        (int, wajib)  : jumlah slogan yang diinginkan (1–10)
      - language     (str, opsional): "id" | "en" | "both" (default: "id")
    """
    data = request.get_json()

    entity_name = data.get("entity_name", "").strip()
    description = data.get("description", "").strip()
    core_values = data.get("core_values", "").strip()
    total = data.get("total")
    language = data.get("language", "id").strip().lower()

    # Validasi input
    if not entity_name:
        return jsonify({"error": "entity_name wajib diisi"}), 400
    if not description:
        return jsonify({"error": "description wajib diisi"}), 400
    if not core_values:
        return jsonify({"error": "core_values wajib diisi"}), 400
    if total is None:
        return jsonify({"error": "total wajib diisi"}), 400
    if not isinstance(total, int) or total <= 0:
        return jsonify({"error": "total harus berupa angka lebih besar dari 0"}), 400
    if total > 10:
        return jsonify({"error": "total maksimal 10"}), 400
    if language not in ("id", "en", "both"):
        return jsonify({"error": "language harus salah satu dari: id, en, both"}), 400

    try:
        result = create_slogans(entity_name, description, core_values, language, total)
        return jsonify({
            "entity_name": entity_name,
            "language": language,
            "total": len(result),
            "data": result,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@slogan_bp.route("/slogans", methods=["GET"])
def get_all():
    """
    GET /slogans?page=1&per_page=20
    Ambil semua slogan yang tersimpan.
    """
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=100, type=int)
    data = get_all_slogans(page=page, per_page=per_page)
    return jsonify(data)


@slogan_bp.route("/slogans/<int:slogan_id>", methods=["GET"])
def get_detail(slogan_id):
    """
    GET /slogans/<id>
    Ambil detail slogan beserta metadata request-nya.
    """
    slogan = get_slogan_by_id(slogan_id)
    if not slogan:
        return jsonify({"error": f"Slogan dengan id {slogan_id} tidak ditemukan"}), 404
    return jsonify(slogan)
