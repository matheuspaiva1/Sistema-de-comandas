from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.domains.produto.produto_service import list_products
import zipfile
import csv
import io
from io import BytesIO

router = APIRouter(prefix="/export/produtos", tags=["Export Produtos"])

@router.get("/csv")
def export_csv():
    def generator():
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        writer.writerow(["id", "name", "description", "price", "active"])
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)

        page = 1
        page_size = 100

        while True:
            data = list_products(page, page_size)
            if not data:
                break
            for row in data:
                writer.writerow(row.values())
                yield buffer.getvalue()
                buffer.seek(0)
                buffer.truncate(0)

            page += 1

    return StreamingResponse(
        generator(),
        media_type="text/csv",
    )

@router.get("/csv-zip")
def export_csv_zip():
    def generator():
        buffer = BytesIO()
        with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zip_file:
            csv_buffer = io.StringIO()
            writer = csv.writer(csv_buffer)
            writer.writerow(["id", "name", "description", "price", "active"])

            page = 1
            page_size = 100

            while True:
                data = list_products(page, page_size)
                if not data:
                    break
                for row in data:
                    writer.writerow(row.values())

                page += 1

            zip_file.writestr("produtos.csv", csv_buffer.getvalue())
        buffer.seek(0)
        yield buffer.read()

    return StreamingResponse(
        generator(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=produtos.zip"}
    )