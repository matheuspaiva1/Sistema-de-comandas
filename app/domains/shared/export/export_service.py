import csv
import zipfile
import io

class ExportService:

    def __init__(self, repo):
        self.repo = repo

    def stream_csv(self):

        def generator():
            buffer = io.StringIO()
            writer = csv.writer(buffer)

            first = True

            for batch in self.repo.iter_batches():
                rows = batch.to_pylist()

                if first and rows:
                    headers = list(rows[0].keys())
                    writer.writerow(headers)
                    yield buffer.getvalue()
                    buffer.seek(0)
                    buffer.truncate(0)
                    first = False

                for row in rows:
                    writer.writerow([row[h] for h in headers])
                    yield buffer.getvalue()
                    buffer.seek(0)
                    buffer.truncate(0)

        return generator()

    def stream_zip(self):

        def generator():
            buffer = io.BytesIO()

            with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
                with zipf.open("dados.csv", "w") as csv_file:

                    first = True

                    for batch in self.repo.iter_batches():
                        rows = batch.to_pylist()

                        if not rows:
                            continue

                        if first:
                            headers = list(rows[0].keys())
                            line = ",".join(headers) + "\n"
                            csv_file.write(line.encode("utf-8"))
                            first = False

                        for row in rows:
                            line = ",".join(str(row[h]) for h in headers) + "\n"
                            csv_file.write(line.encode("utf-8"))

            buffer.seek(0)
            yield buffer.read()

        return generator()