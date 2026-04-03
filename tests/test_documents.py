import io


def _create_dummy_pdf() -> bytes:
    """Create a minimal valid PDF for testing."""
    # Minimal PDF with one blank page
    return (
        b"%PDF-1.4\n"
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n"
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] >>\nendobj\n"
        b"xref\n0 4\n"
        b"0000000000 65535 f \n"
        b"0000000009 00000 n \n"
        b"0000000058 00000 n \n"
        b"0000000115 00000 n \n"
        b"trailer\n<< /Root 1 0 R /Size 4 >>\n"
        b"startxref\n190\n%%EOF"
    )


def test_upload_document(client, analyst_headers):
    pdf_data = _create_dummy_pdf()
    response = client.post(
        "/documents/upload",
        files={"file": ("test.pdf", io.BytesIO(pdf_data), "application/pdf")},
        data={"title": "Test Report", "document_type": "annual_report", "company_name": "TestCorp"},
        headers=analyst_headers,
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Report"


def test_list_documents(client, auth_headers):
    response = client.get("/documents/", headers=auth_headers)
    assert response.status_code == 200
    assert "documents" in response.json()


def test_client_cannot_upload(client, auth_headers):
    pdf_data = _create_dummy_pdf()
    response = client.post(
        "/documents/upload",
        files={"file": ("test.pdf", io.BytesIO(pdf_data), "application/pdf")},
        data={"title": "Test"},
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_search_documents(client, auth_headers):
    response = client.get("/documents/search?title=test", headers=auth_headers)
    assert response.status_code == 200
