from fastapi.staticfiles import StaticFiles

def mount_uploaded_files(app):
    UPLOAD_DIRECTORY = "app/uploads"
    app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

def mount_generated_pdf(app):
    UPLOAD_DIRECTORY = "app/generated_pdf"
    app.mount("/pdf", StaticFiles(directory=UPLOAD_DIRECTORY), name="generated_pdf")