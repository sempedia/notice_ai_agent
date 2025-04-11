import pytest
import datetime
from chains.notice_email_extraction import NoticeEmailExtract


# ✅ Test 1: Handle numeric fields correctly
def test_notice_email_numeric_fields():
    email_data = NoticeEmailExtract(project_id=987654321, max_potential_fine=15000.75)
    assert email_data.project_id == 987654321
    assert email_data.max_potential_fine == 15000.75




# ✅ Test 2: Handle negative and zero fines correctly
def test_notice_email_negative_fines():
    email_data = NoticeEmailExtract(max_potential_fine=-5000.0)
    assert email_data.max_potential_fine == -5000.0  # Should allow negative numbers (but might not be realistic)



# ✅ Test 3: Handle non-numeric inputs in numeric fields (should raise error)
def test_notice_email_invalid_numeric_input():
    with pytest.raises(ValueError):
        NoticeEmailExtract(project_id="abc123")  # Should raise an error


